# BLACKJACK
# By Alexander Belyakov
# blackjack.py
# ver 1.0 / 31 May 2021

import random

INITIAL_CASH = 100.0

def main():
    """
    () -> None
    
    Print welcome message and set initial cash.
    While player has cash, offer to place a bet, then play a game round.
    After player runs out of cash or places a zero-sized bet, print farewell message.
    """
    
    cash = INITIAL_CASH
    print_welcome_message(cash)

    while cash:
        bet = get_player_bet(cash)
        if bet == 0:
            break
        cash += play_round(bet, cash)

    print_farewell_message(cash)
    input()


def print_welcome_message(cash):
    """
    (int) -> None
    
    Print welcome message and offer player a chance to read game rules.
    """

    print()
    print("+--------------------------------------+")
    print("|                                      |")
    print("|         WELCOME TO BLACKJACK!        |")
    print("|                                      |")
    print("+--------------------------------------+\n")
    
    print("Player starts the game with ${:.2f}.\n".format(cash))

    game_rules()
    
    print("Good luck!\n")


def game_rules():
    """
    () -> None

    Print game rules if player wants to read them.
    """

    answer = input("Do you want to read the game rules? (y/n): ").strip().lower()

    while answer not in ["y", "n", "yes", "no"]:
        answer = input("Invalid input. Do you want to read the game rules? (y/n): ").strip().lower()
    print()

    if answer in ["n", "no"]:
        return

    print("GAME RULES:\n")
    print("  1. The player places a bet. A zero-sized bet ends the game.\n")
    print("  2. Both the player and the dealer are dealt two cards each.")
    print("     Only the first dealer card is visible.\n")
    print("  3. If the first dealer card is an Ace,")
    print("     the player may buy insurance at 1/2 the bet amount.\n")
    print("  4. If the dealer has a natural blackjack, the player loses:")
    print("      - If the player also has a natural blackjack, it is a push.")
    print("      - If the player has insurance, they win the insurance bet at")
    print("        a 2-to-1 ratio, effectively preventing their loss.\n")
    print("  5. If the player has two cards of equal value, they may split their hand")
    print("     into two by doubling their bet. Both hands are then played separately.\n")
    print("  6. If the player has a natural blackjack, they win at a 3-to-2 ratio,")
    print("     unless it's a split hand, in which case the payout is at a 1-to-1 ration.\n")
    print("  7. If there is no natural blackjack on the table,")
    print("     the player may hit, stand, double or surrender:")
    print("      - 'Hit' means draw another card.")
    print("      - 'Stand' means stop drawing.")
    print("        This happens automatically if the player has 21 or more points.")
    print("      - 'Double' means double the bet and draw only one more card.")
    print("        This option is available only before any additional cards are drawn.")
    print("      - 'Surrender' means fold your hand but lose only 1/2 the bet amount.")
    print("        This option is available only before any additional cards are drawn.\n")
    print("  8. If the player has more than 21 points, they bust and lose their bet.\n")
    print("  9. Otherwise, the dealer draws cards until they have 17 or more points.\n")
    print(" 10. If the dealer has more than 21 points, they bust and the player wins")
    print("     at a 1-to-1 ratio.\n")
    print(" 11. Otherwise, the higher score wins, whereas tied scores are a push:")
    print("      - Jacks, Queens and Kings are worth 10 points.")
    print("      - Aces are worth either 11 points or 1 point,")
    print("        depending on the situation.")
    print("      - All other cards are worth their face value.\n")


def get_player_bet(cash):
    """
    (int) -> int
    
    Print amount of available cash.
    Return valid bet (bets must be whole, positive and can't exceed available cash).
    """

    print("------------ PLACE YOUR BET ------------\n")
    print("You have ${:.2f}.".format(cash))
    bet = input("Please enter your bet (0 to leave table): ").strip()

    while not bet.isdigit() or int(bet) < 0 or int(bet) > cash:
        if not bet.isdigit():
            if bet[0] == '-' and bet[1:].isdigit():
                print("Your bet must be positive. ", end="")
            elif "." in bet and bet.replace('.', '', 1).isdigit():
                print("Your bet must be whole. ", end="")
            else:
                print("Invalid bet. ", end="")
        elif int(bet) > cash:
            print("You can't bet more than you have. ", end="")

        bet = input("Please enter valid bet (0 to leave table): ").strip()

    print()
    return int(bet)


def play_round(bet, cash):
    """
    (int, int) -> int
    
    Create 52-card deck and shuffle it.
    Deal two cards each to player and dealer.
    Check for insurance availability (first dealer's card is an Ace and player had enough cash).
    Check for dealer blackjack (dealer has natural 21).
    Check for player blackjack (player has natural 21).
    Allow player to split hand of two equal-value cards.
    Allow player to double or surrender, otherwise hit until he stands or busts.
    If player doesn't bust, draw until dealer reaches 17 or busts.
    Return cash result based on player's and dealer's hands.
    """
    
    deck = create_shuffled_deck()
    player_hand, dealer_hand = deal_cards(deck)
    insurance = False

    if dealer_hand[0][0] == "A" and cash >= bet / 2:
        print_cards(player_hand, dealer_hand)
        insurance = get_insurance(bet)

    if get_hand_value(dealer_hand) == 21 or get_hand_value(player_hand) == 21:
        print_cards(player_hand, dealer_hand, hidden=False)
        return round_result(player_hand, dealer_hand, bet, insurance)

    if get_hand_value([player_hand[0]]) == get_hand_value([player_hand[1]]) and cash >= bet * 2:
        print_cards(player_hand, dealer_hand)
        
        if get_split(bet):
            player_hand_1, player_hand_2 = split_hand(player_hand, deck)
            print_cards([player_hand_1, player_hand_2], dealer_hand, split=True)
            print("-------------- FIRST HAND --------------")
            choice_1 = player_decision(player_hand_1, dealer_hand, deck, bet, cash)
            print("-------------- SECOND HAND -------------")
            choice_2 = player_decision(player_hand_2, dealer_hand, deck, bet, cash)
            
            if choice_1 == "sur" and choice_2 == "sur":
                return -bet
            
            if (get_hand_value(player_hand_1) <= 21 and choice_1 != "sur") or (get_hand_value(player_hand_2) <= 21 and choice_2 != "sur"):
                dealer_decision([player_hand_1 if choice_1 != "sur" else [], player_hand_2 if choice_2 != "sur" else []], dealer_hand, deck, split=True)

            return split_round_result(player_hand_1, choice_1, player_hand_2, choice_2, dealer_hand, bet, insurance)

    choice = player_decision(player_hand, dealer_hand, deck, bet, cash)

    if choice == "sur":
        return -bet / 2
    
    if choice == "dou":
        bet = bet * 2 if bet * 2 <= cash else cash

    if get_hand_value(player_hand) <= 21:
        dealer_decision(player_hand, dealer_hand, deck)

    return round_result(player_hand, dealer_hand, bet, insurance)


def deal_cards(deck):
    """
    (list) -> (list, list)

    Deal two cards each to player and dealer.
    Return card hands.
    """
    
    player_hand = ['10?', '10?']
    # player_hand.append(deck.pop())
    # player_hand.append(deck.pop())

    dealer_hand = []
    dealer_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    
    return (player_hand, dealer_hand)


def get_insurance(bet):
    """
    (int) -> bool
    
    Allow player to receive insurance at half price.
    """

    print("-------- DO YOU WANT INSURANCE? --------\n")
    answer = input("Do you want insurance against the dealer having blackjack for ${:.2f}? (y/n): ".format(bet / 2)).strip().lower()

    while answer not in ["y", "n", "yes", "no"]:
        answer = input("Invalid input. Do you want insurance for ${:.2f}? (y/n): ".format(bet / 2)).strip().lower()

    print()
    return True if answer in ["y", "yes"] else False


def get_split(bet):
    """
    (int) -> bool
    
    Allow player to split hand.
    """

    print("--------- DO YOU WANT TO SPLIT? --------\n")
    answer = input("Do you want to split your hand into two for an additional ${:.2f}? (y/n): ".format(bet)).strip().lower()

    while answer not in ["y", "n", "yes", "no"]:
        answer = input("Invalid input. Do you want to split your hand for ${:.2f}? (y/n): ".format(bet)).strip().lower()

    print()
    return True if answer in ["y", "yes"] else False


def split_hand(hand, deck):
    """
    (list, list) -> (list, list)

    Split one two-card hand into two two-card hands.
    """

    player_hand_1 = [hand[0]]
    player_hand_1.append(deck.pop())
    
    player_hand_2 = [hand[1]]
    player_hand_2.append(deck.pop())

    return (player_hand_1, player_hand_2)


def player_decision(player_hand, dealer_hand, deck, bet, cash):
    """
    (list, list, list, int, int) -> str
    
    Show player's cards and dealer's first card.
    Allow player to hit until he stands or busts.
    Allow player to surrender or double before first card is drawn.
    Return player's choice.
    """

    print("------------- PLAYER CHOICE ------------\n")
    print_cards(player_hand, dealer_hand)
    choice = None
    while get_hand_value(player_hand) < 21:
        choice = get_choice(player_hand)

        if choice == "sta":
            break
        
        if choice == "sur":
            print("You surrendered. You lose ${:.2f}.\n".format(bet / 2))
            break
        
        if choice == "dou":
            print("You doubled your bet to ${:.2f}.\n".format(bet * 2 if bet * 2 <= cash else cash))
            
        player_hand.append(deck.pop())
        print_cards(player_hand, dealer_hand)
        
        if choice == "dou":
            break

    return choice


def dealer_decision(player_hand, dealer_hand, deck, split=False):
    """
    (list, list, list) -> None
    
    Show player's and dealer's cards.
    Deal cards until dealer reaches 17 or busts.
    """

    print("------------- DEALER'S DRAW ------------\n")
    while get_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    print_cards(player_hand, dealer_hand, hidden=False, split=split)


def round_result(player_hand, dealer_hand, bet, insurance, split=False):
    """
    (int, int, int, bool, bool) -> int

    Check dealer's natural blackjack with/without player's blackjack and with/without insurance.
    Check player's natural blackjack.
    Print player's results and dealer's result if player didn't bust.
    Print and return player's cash gain or loss.
    """

    player_score = get_hand_value(player_hand)
    dealer_score = get_hand_value(dealer_hand)

    print("---------------- RESULTS ---------------\n")

    if dealer_score == 21 and len(dealer_hand) == 2:
        if player_score == 21:
            print("Both you and dealer have blackjack.")
            if insurance:
                print("You have insurance, so you win ${:.2f}.\n".format(bet * 1.5))
                return bet * 1.5
            print("It's a push.\n")
            return 0
        print("Dealer has blackjack.")
        if insurance:
            print("You have insurance, so you come out even.\n")
            return 0
        print("You lose ${:.2f}.\n".format(bet))
        return -bet

    if player_score == 21 and len(player_hand) == 2:
        print("You have blackjack.")
        if split:
            print("You win ${:.2f}.\n".format(bet))
            return bet
        print("You win ${:.2f}.\n".format(bet * 1.5))
        return bet * (1.5 - 0.5 * insurance)
    
    print(f"You have {player_score}", end="")
    print("." if player_score > 21 else f", dealer has {dealer_score}.")

    if player_score > 21:
        print("You busted. You lose ${:.2f}.\n".format(bet))
        return -bet * (1 + 0.5 * insurance * (not split))

    if dealer_score > 21:
        print("Dealer busted. You win ${:.2f}.\n".format(bet))
        return bet * (1 - 0.5 * insurance * (not split))

    if dealer_score > player_score:
        print("Dealer wins. You lose ${:.2f}.\n".format(bet))
        return -bet * (1 + 0.5 * insurance * (not split))

    if dealer_score < player_score:
        print("You win ${:.2f}.\n".format(bet))
        return bet * (1 - 0.5 * insurance * (not split))

    print("It's a push.\n")
    return -bet * 0.5 * insurance * (not split)


def split_round_result(player_hand_1, choice_1, player_hand_2, choice_2, dealer_hand, bet, insurance):
    """
    (list, str, list, str, list, int, bool) -> int

    Calculates results for each player hand, returns combined player's cash gain or loss.
    """

    if choice_1 == "sur":
        result_1 = -bet / 2
    else:
        print("-------------- FIRST HAND --------------")
        result_1 = round_result(player_hand_1, dealer_hand, bet * 2 if choice_1 == "dou" else bet, insurance, split=True)

    if choice_2 == "sur":
        result_2 = -bet / 2
    else:
        print("-------------- SECOND HAND -------------")
        result_2 = round_result(player_hand_2, dealer_hand, bet * 2 if choice_2 == "dou" else bet, insurance, split=True)

    return result_1 + result_2 - 0.5 * bet * insurance


def create_shuffled_deck():
    """
    () -> list

    Create, shuffle and return deck of 52 cards.
    """
    
    deck = []
    
    for suit in ["♠", "♥", "♦", "♣"]:
        for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            deck.append(value + suit)

    random.shuffle(deck)
    return deck


def get_hand_value(hand):
    """
    (list) -> int

    Calculate and return value of hand (Aces count as 1's or 11's depending on situation).
    """
    
    value = 0
    aces = 0

    for card in hand:
        if card[0] in ["1", "J", "Q", "K"]:
            value += 10
        elif card[0] != "A":
            value += int(card[0])
        else:
            aces += 1

    for i in range(aces):
        value += 11 if value <= 11 - aces else 1

    return value


def print_cards(player_hand, dealer_hand, hidden=True, split=False):
    """
    (list, list, bool) -> None

    Print pseudographic cards in player's and dealer's hands.
    If hand is split, print both player's hands.
    If dealer's hand is hidden, print only first card of dealer's hand.
    """

    if split and player_hand[0]:
        print("YOUR FIRST HAND:")
        print_hand(player_hand[0])

    if split and player_hand[1]:
        print("YOUR SECOND HAND:")
        print_hand(player_hand[1])

    if not split:
        print("YOUR HAND:")
        print_hand(player_hand)
    
    print("DEALER'S HAND:")
    print_hand(dealer_hand, hidden=hidden)


def print_hand(hand, hidden=False):
    """
    (list, bool) -> None

    Print pseudographic card hand.
    If hand is hidden, print only first card in hand.
    """

    print("+-----+ " * len(hand))
    print(' '.join(["|" + value[:-1] + " " * (5 - len(value[:-1])) + "|" for value in hand]) if not hidden else "|" + hand[0][:-1] + " " * (5 - len(hand[0][:-1])) + "| " + "|xxxxx| " * (len(hand) - 1))
    print("|     | " * len(hand) if not hidden else "|     | " + "|xxxxx| " * (len(hand) - 1))
    print(' '.join(["|  " + value[-1] + "  |" for value in hand]) if not hidden else "|  " + hand[0][-1] + "  | " + "|xxxxx| " * (len(hand) - 1))
    print("|     | " * len(hand) if not hidden else "|     | " + "|xxxxx| " * (len(hand) - 1))
    print(' '.join(["|" + " " * (5 - len(value[:-1])) + value[:-1] + "|" for value in hand]) if not hidden else "|" + " " * (5 - len(hand[0][:-1])) + hand[0][:-1] + "| " + "|xxxxx| " * (len(hand) - 1))
    print("+-----+ " * len(hand))
    print()


def get_choice(player_hand):
    """
    (list) -> str

    Return "hit", "sta", "dou" or "sur" (two latter options available only if player hasn't drawn a card yet).
    """

    if len(player_hand) == 2:
        choice = input("Do you want to hit, stand, double or surrender? ").strip()[:3].lower()
        while choice not in ["hit", "sta", "dou", "sur"]:
            choice = input("Invalid input. Do you want to hit, stand, double or surrender? ").strip()[:3].lower()
    else:
        choice = input("Do you want to hit or stand? ").strip()[:3].lower()
        while choice not in ["hit", "sta"]:
            choice = input("Invalid input. Do you want to hit or stand? ").strip()[:3].lower()

    print()
    return choice


def print_farewell_message(cash):
    """
    (int) -> None

    Print amount of cash at end of game and positive/negative difference.
    Print farewell message.
    """

    print("--------------- GAME OVER --------------\n")
    print("You leave the table with ${:.2f}.".format(cash))
    if cash < INITIAL_CASH:
        print("You have lost ${:.2f}.".format(INITIAL_CASH - cash))
    elif cash > INITIAL_CASH:
        print("You have won ${:.2f}.".format(cash - INITIAL_CASH))
    else:
        print("You haven't won or lost anything.")
    print("\nThank you for playing!\n")

if __name__ == '__main__':
    main()
