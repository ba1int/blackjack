import random

# Define the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11 represents Ace

# Define ASCII art representations of card suits
suits_ascii = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

def create_deck():
    return [{'value': value, 'suit': suit} for value in values for suit in suits]

# Function to calculate the hand value
def calculate_value(hand):
    value = sum(card['value'] for card in hand)
    num_aces = sum(1 for card in hand if card['value'] == 11)

    while num_aces > 0 and value > 21:
        value -= 10
        num_aces -= 1

    return value

# Function to display cards in ASCII art
def display_hand(hand, is_dealer=False, hide_first_card=True):
    card_lines = [[] for _ in range(7)]

    for card in hand:
        value = card['value']
        suit = suits_ascii[card['suit']]
        card_ascii = f"┌───────┐\n" \
                     f"| {value: <2}    |\n" \
                     f"|       |\n" \
                     f"|   {suit}   |\n" \
                     f"|       |\n" \
                     f"|    {value: >2} |\n" \
                     f"└───────┘"

        if is_dealer and hide_first_card and card == hand[0]:
            card_ascii = f"┌───────┐\n" \
                         f"|░░░░░░░░|\n" \
                         f"|░░░░░░░░|\n" \
                         f"|░░░░░░░░|\n" \
                         f"|░░░░░░░░|\n" \
                         f"|░░░░░░░░|\n" \
                         f"└───────┘"

        card_lines_split = card_ascii.split('\n')
        for i in range(7):
            card_lines[i].append(card_lines_split[i])

    for line in card_lines:
        print(" ".join(line))

    if not is_dealer:
        print(f"Hand Value: {calculate_value(hand)}")

# Function to draw a card from the deck and remove it from the deck
def draw_card(deck, drawn_cards):
    remaining_cards = [card for card in deck if card not in drawn_cards]
    if not remaining_cards:
        # If all cards have been drawn, reshuffle the deck
        remaining_cards = create_deck()
    card = random.choice(remaining_cards)
    drawn_cards.append(card)
    return card

# Initial deal of cards
def start_game(deck, drawn_cards):
    player_hand = [draw_card(deck, drawn_cards) for _ in range(2)]
    dealer_hand = [draw_card(deck, drawn_cards) for _ in range(2)]
    return player_hand, dealer_hand

# Main game loop
def game():
    bankroll = int(input("Deposit: "))  # Initial bankroll
    streak = 0  # Initialize the winning streak counter
    max_streak = 0  # Initialize the maximum winning streak counter
    drawn_cards = []  # Keep track of drawn cards

    while bankroll > 0:
        deck = create_deck()
        player_hand, dealer_hand = start_game(deck, drawn_cards)

        bet_input = input(f"Current bankroll: ${bankroll}. Enter your bet (type 'exit' to quit): ")

        if bet_input.lower() in ['exit', 'quit', 'q']:
            break

        try:
            bet = int(bet_input)
            if bet > bankroll:
                print("Not enough money. Please enter a valid bet.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid bet or type 'exit' to quit.")
            continue

        # Display initial cards
        print("Player's Hand:")
        display_hand(player_hand)
        print("\nDealer's Hand:")
        display_hand(dealer_hand, is_dealer=True)

        # Check for blackjack
        if calculate_value(player_hand) == 21:
            winnings = int(bet * 2.5)
            print(f"Blackjack! You win ${winnings}!")
            bankroll += winnings
            streak += 1
        else:
            # Player can choose to hit or stand
            while True:
                choice = input("\nDo you want to hit (h) or stand (s)? ").lower()

                if choice == 'h' or choice == 'hit':
                    new_card = draw_card(deck, drawn_cards)
                    player_hand.append(new_card)
                    print(f"You drew a {new_card['value']} of {new_card['suit']}.")
                    display_hand(player_hand)

                    # Check for player bust
                    if calculate_value(player_hand) > 21:
                        print(f"Too much! You lose ${bet}.")
                        bankroll -= bet
                        streak = 0  # Reset the streak on a loss
                        break
                elif choice == 's' or choice == 'stand':
                    # Dealer's turn
                    while calculate_value(dealer_hand) < 17:
                        new_card = draw_card(deck, drawn_cards)
                        dealer_hand.append(new_card)

                    print("\nDealer's Hand:")
                    display_hand(dealer_hand)
                    print("Dealer's Hand Value:", calculate_value(dealer_hand))

                    # Determine the winner
                    if calculate_value(dealer_hand) > 21:
                        print(f"Dealer busts! You win ${bet}!")
                        bankroll += bet
                        streak += 1
                    elif calculate_value(dealer_hand) == calculate_value(player_hand):
                        print("It's a draw. You get your bet back.")
                    elif calculate_value(dealer_hand) >= calculate_value(player_hand):
                        print("Dealer wins.")
                        bankroll -= bet
                        streak = 0  # Reset the streak on a loss
                    else:
                        print(f"You win ${bet}!")
                        bankroll += bet
                        streak += 1

                    if streak > max_streak:
                        max_streak = streak

                    break
                else:
                    print("Invalid choice. Please choose 'h' to hit or 's' to stand.")

        if bankroll <= 0:
            print("Your bankroll is busted. Game over.")
            break

        print(f"Current winning streak: {streak} games")
        print(f"Maximum winning streak: {max_streak} games")

if __name__ == '__main__':
    game()
