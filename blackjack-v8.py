import random

# Define the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11 represents Ace

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

# Function to display cards
def display_hand(hand, is_dealer=False, hide_first_card=True):
    if is_dealer and hide_first_card:
        # Display the first card as "Hidden Card"
        print("Hidden Card")
        for card in hand[1:]:
            print(f"{card['value']} of {card['suit']}")
    else:
        for card in hand:
            print(f"{card['value']} of {card['suit']}")
    
    if not is_dealer:
        print(f"Hand Value: {calculate_value(hand)}")

# Function to draw a card from the deck
def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

# Initial deal of cards
def start_game(deck):
    player_hand = [draw_card(deck) for _ in range(2)]
    dealer_hand = [draw_card(deck) for _ in range(2)]
    return player_hand, dealer_hand

# Main game loop
def game():
    bankroll = 1000  # Initial bankroll
    while bankroll > 0:
        deck = create_deck()
        player_hand, dealer_hand = start_game(deck)
        
        bet_input = input(f"Current bankroll: ${bankroll}. Enter your bet (type 'exit' to quit): ")
        
        if bet_input.lower() == 'exit':
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
            winnings = int(bet * 1.5)
            print(f"Blackjack! You win ${winnings}!")
            bankroll += winnings
        else:
            # Player can choose to hit or stand
            while True:
                choice = input("\nDo you want to hit or stand? ").lower()

                if choice == 'hit':
                    new_card = draw_card(deck)
                    player_hand.append(new_card)
                    print(f"You drew a {new_card['value']} of {new_card['suit']}.")
                    display_hand(player_hand)

                    # Check for player bust
                    if calculate_value(player_hand) > 21:
                        print(f"Too much! You lose ${bet}.")
                        bankroll -= bet
                        break
                elif choice == 'stand':
                    # Dealer's turn
                    while calculate_value(dealer_hand) < 17:
                        new_card = draw_card(deck)
                        dealer_hand.append(new_card)

                    print("\nDealer's Hand:")
                    display_hand(dealer_hand)
                    print("Dealer's Hand Value:", calculate_value(dealer_hand))

                    # Determine the winner
                    if calculate_value(dealer_hand) > 21:
                        print(f"Dealer busts! You win ${bet}!")
                        bankroll += bet
                    elif calculate_value(dealer_hand) == calculate_value(player_hand):
                        print("It's a draw. You get your bet back.")
                    elif calculate_value(dealer_hand) >= calculate_value(player_hand):
                        print("Dealer wins.")
                        bankroll -= bet
                    else:
                        print(f"You win ${bet}!")
                        bankroll += bet

                    break
                else:
                    print("Invalid choice. Please choose 'hit' or 'stand.")
                    
        if bankroll <= 0:
            print("Your bankroll is busted. Game over.")
            break

if __name__ == '__main__':
    game()
