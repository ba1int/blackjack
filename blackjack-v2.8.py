import random

# Define the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11 represents Ace

# Define ASCII art representations of card suits
suits_ascii = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

# Diamond back pattern
diamond_back = "┌───────┐\n" \
              "│♦♦♦♦♦♦♦│\n" \
              "│♦♦♦♦♦♦♦│\n" \
              "│♦♦♦♦♦♦♦│\n" \
              "│♦♦♦♦♦♦♦│\n" \
              "│♦♦♦♦♦♦♦│\n" \
              "└───────┘"

def create_deck(num_decks):
    single_deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
    return single_deck * num_decks

def calculate_value(hand):
    value = sum(card['value'] for card in hand)
    num_aces = sum(1 for card in hand if card['value'] == 11)

    while num_aces > 0 and value > 21:
        value -= 10
        num_aces -= 1

    return value

# Function to display cards in ASCII art with a diamond back design
def display_hand_with_diamond_back(hand, is_dealer=False, hide_first_card=True):
    card_lines = []

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
            card_ascii = diamond_back

        card_lines_split = card_ascii.split('\n')
        for i in range(7):
            card_lines.append(card_lines_split[i])

    for i in range(7):
        for j in range(len(hand)):
            print(card_lines[j * 7 + i], end=' ')
        print()

    if not is_dealer:
        print(f"Hand Value: {calculate_value(hand)}")

# Function to draw a card from the deck
def draw_card(deck):
    return deck.pop()

# Initial deal of cards
def start_game(deck):
    player_hand = [draw_card(deck) for _ in range(2)]
    dealer_hand = [draw_card(deck) for _ in range(2)]
    split_hands = []  # List to hold split hands

    return player_hand, dealer_hand, split_hands

# Split a pair into two separate hands
def split_pair(player_hand, split_hands, deck):
    if len(player_hand) == 2 and player_hand[0]['value'] == player_hand[1]['value']:
        # Check if the first two cards form a pair
        split_hands.append([player_hand.pop()])  # Move one card to the split hand
        split_hands[-1].append(draw_card(deck))  # Draw a new card for the split hand
        player_hand.append(draw_card(deck))  # Draw a new card for the original hand
        return True
    return False

# Main game loop
def game():
    num_decks = int(input("Enter the number of decks to use: "))
    deck = create_deck(num_decks)  # Create a shared deck
    bankroll = float(input("Deposit: "))  # Initial bankroll (accepts float values)
    streak = 0  # Initialize the winning streak counter
    max_streak = 0  # Initialize the maximum winning streak counter
    hands_played = 0  # Initialize the hands played counter

    while bankroll > 0:
        random.shuffle(deck)  # Shuffle the deck
        player_hand, dealer_hand, split_hands = start_game(deck)
        hands_played += 1  # Increment the hands played counter

        bet_input = input(f"Hand {hands_played}: Current bankroll: ${bankroll:.2f}. Enter your bet (type 'exit' to quit): ")

        if bet_input.lower() in ['exit', 'quit', 'q']:
            break

        try:
            bet = float(bet_input)  # Accept float bet amounts
            if bet > bankroll:
                print("Not enough money. Please enter a valid bet.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid bet or type 'exit' to quit.")
            continue

        # Display initial cards
        print("Player's Hand:")
        display_hand_with_diamond_back(player_hand)
        print("\nDealer's Hand:")
        display_hand_with_diamond_back(dealer_hand, is_dealer=True)

        # Check for blackjack
        if calculate_value(player_hand) == 21:
            winnings = bet * 1.5
            print(f"Blackjack! You win ${winnings:.2f}!")
            bankroll += winnings
            streak += 1
            if streak > max_streak:
                max_streak = streak  # Update max_streak immediately
        else:
            # Player can choose to hit, stand, double down, or split pairs
            while True:
                choice = input("\nDo you want to hit (h), stand (s), double down (d), or split pairs (p)? ").lower()

                if choice == 'h' or choice == 'hit':
                    new_card = draw_card(deck)  # Draw from the shared deck
                    if not new_card:
                        break  # No cards left
                    player_hand.append(new_card)
                    print(f"You drew a {new_card['value']} of {new_card['suit']}.")
                    display_hand_with_diamond_back(player_hand)

                    # Check for player bust
                    if calculate_value(player_hand) > 21:
                        print(f"Too much! You lose ${bet:.2f}.")
                        bankroll -= bet
                        streak = 0  # Reset the streak on a loss
                        break
                elif choice == 's' or choice == 'stand':
                    # Dealer's turn
                    while calculate_value(dealer_hand) < 17:
                        new_card = draw_card(deck)  # Draw from the shared deck
                        if not new_card:
                            break  # No cards left
                        dealer_hand.append(new_card)

                    print("\nDealer's Hand:")
                    display_hand_with_diamond_back(dealer_hand)
                    print("Dealer's Hand Value:", calculate_value(dealer_hand))

                    # Determine the winner
                    if calculate_value(dealer_hand) > 21:
                        print(f"Dealer busts! You win ${bet:.2f}!")
                        bankroll += bet
                        streak += 1
                        if streak > max_streak:
                            max_streak = streak  # Update max_streak immediately
                    elif calculate_value(dealer_hand) == calculate_value(player_hand):
                        print("It's a draw. You get your bet back.")
                        bankroll += bet  # Return the bet to the player
                    elif calculate_value(dealer_hand) >= calculate_value(player_hand):
                        print("Dealer wins.")
                        bankroll -= bet
                        streak = 0  # Reset the streak on a loss
                    else:
                        print(f"You win ${bet:.2f}!")
                        bankroll += bet
                        streak += 1
                        if streak > max_streak:
                            max_streak = streak  # Update max_streak immediately

                    break
                elif choice == 'd' or choice == 'double down':
                    bet *= 2
                    new_card = draw_card(deck)  # Draw from the shared deck
                    if not new_card:
                        break  # No cards left
                    player_hand.append(new_card)
                    print(f"You drew a {new_card['value']} of {new_card['suit']}.")
                    display_hand_with_diamond_back(player_hand)

                    # Check for player bust
                    if calculate_value(player_hand) > 21:
                        print(f"Too much! You lose ${bet:.2f}.")
                        bankroll -= bet
                        streak = 0  # Reset the streak on a loss
                    else:
                        # Dealer's turn
                        while calculate_value(dealer_hand) < 17:
                            new_card = draw_card(deck)  # Draw from the shared deck
                            if not new_card:
                                break  # No cards left
                            dealer_hand.append(new_card)

                        print("\nDealer's Hand:")
                        display_hand_with_diamond_back(dealer_hand)
                        print("Dealer's Hand Value:", calculate_value(dealer_hand))

                        # Determine the winner
                        if calculate_value(dealer_hand) > 21:
                            print(f"Dealer busts! You win ${bet:.2f}!")
                            bankroll += bet
                            streak += 1
                            if streak > max_streak:
                                max_streak = streak  # Update max_streak immediately
                        elif calculate_value(dealer_hand) == calculate_value(player_hand):
                            print("It's a draw. You get your bet back.")
                            bankroll += bet  # Return the bet to the player
                        elif calculate_value(dealer_hand) >= calculate_value(player_hand):
                            print("Dealer wins.")
                            bankroll -= bet
                            streak = 0  # Reset the streak on a loss
                        else:
                            print(f"You win ${bet:.2f}!")
                            bankroll += bet
                            streak += 1
                            if streak > max_streak:
                                max_streak = streak  # Update max_streak immediately

                    break
                elif choice == 'p' or choice == 'split pairs':
                    if split_pair(player_hand, split_hands, deck):
                        print("Pair split!")
                        display_hand_with_diamond_back(player_hand, is_dealer=False)
                        for i, hand in enumerate(split_hands):
                            print(f"Split Hand {i + 1}:")
                            display_hand_with_diamond_back(hand, is_dealer=False)

                        # Bet on each split hand
                        for i, hand in enumerate(split_hands):
                            bet_input = input(f"Bet on Split Hand {i + 1}: ")
                            try:
                                split_bet = float(bet_input)
                                if split_bet > bankroll:
                                    print("Not enough money. Please enter a valid bet.")
                                    continue
                                split_hands[i].append(draw_card(deck))  # Draw a card for the split hand
                            except ValueError:
                                print("Invalid input. Please enter a valid bet.")
                                continue

                    else:
                        print("You can only split pairs of the same value.")
                else:
                    print("Invalid choice. Please choose 'h' to hit, 's' to stand, 'd' to double down, or 'p' to split pairs.")

        if bankroll <= 0:
            print("Your bankroll is busted. Game over.")
            break

        print(f"Current winning streak: {streak} games")
        print(f"Maximum winning streak: {max_streak} games")
        print(f"Cards left in the deck: {len(deck):.0f}")

if __name__ == '__main__':
    game()
