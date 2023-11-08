import random

class Card:
    suit_names = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

    def ascii_art(self, hidden=False):
        if hidden:
            return ["┌───────┐"] + ["│░░░░░░░│"] * 5 + ["└───────┘"]

        space = ' ' if len(self.value) == 1 else ''
        value_str = str(self.value).ljust(2, ' ') if len(str(self.value)) == 1 else str(self.value)
        suit_symbol = Card.suit_symbols[self.suit]
        return [
            "┌───────┐",
            f"│{value_str}     │",
            "│       │",
            f"│   {suit_symbol}   │",
            "│       │",
            f"│     {value_str}│",
            "└───────┘"
        ]

class Deck:
    def __init__(self, num_decks=1):
        self.cards = [Card(suit, value) for suit in Card.suit_names for value in Card.values for _ in range(num_decks)]
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None

    def cards_left(self):
        return len(self.cards)

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.value in ['J', 'Q', 'K']:
                value += 10
            elif card.value == 'A':
                aces += 1
                value += 11
            else:
                value += int(card.value)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def display(self, hide_first_card=False):
        lines = ['' for _ in range(7)]
        for i, card in enumerate(self.cards):
            card_lines = card.ascii_art(hidden=hide_first_card and i == 0)
            lines = [l + '  ' + cl for l, cl in zip(lines, card_lines)]
        print('\n'.join(lines))
        if not hide_first_card:
            print(f"Hand value: {self.calculate_value()}")

class Game:
    BLACKJACK_PAYOUT = 1.5

    def __init__(self):
        self.num_decks = int(input("Enter the number of decks to use: "))
        self.deck = Deck(self.num_decks)
        self.bankroll = float(input("Deposit: "))
        self.streak = 0
        self.max_streak = 0
        self.hands_played = 0

    def get_bet(self):
        while True:
            bet_input = input(f"Hand {self.hands_played + 1}: Current bankroll: ${self.bankroll:.2f}. Enter your bet (type 'exit' to quit): ")
            if bet_input.lower() in ['exit', 'quit', 'q']:
                return None
            try:
                bet = float(bet_input)
                if bet > self.bankroll:
                    print("Not enough money. Please enter a valid bet.")
                    continue
                return bet
            except ValueError:
                print("Invalid input. Please enter a valid bet or type 'exit' to quit.")

    def initial_deal(self):
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(self.deck.draw_card())
        player_hand.add_card(self.deck.draw_card())
        dealer_hand.add_card(self.deck.draw_card())
        dealer_hand.add_card(self.deck.draw_card())
        return player_hand, dealer_hand

    def player_turn(self, player_hand, bet):
        player_bust = False
        while True:
            player_value = player_hand.calculate_value()
            if player_value == 21:
                print("Blackjack! Player wins!")
                self.bankroll += bet * self.BLACKJACK_PAYOUT
                self.streak += 1
                return False
            elif player_value > 21:
                print("Bust! Player loses.")
                self.bankroll -= bet
                self.streak = 0
                return True

            choice = input("Do you want to (h)it or (s)tand? ").lower()
            if choice in ['h', 'hit']:
                player_hand.add_card(self.deck.draw_card())
                player_hand.display()
                print(f"Hand value: {player_hand.calculate_value()}")
                if player_hand.calculate_value() > 21:
                    print("Bust! Player loses.")
                    self.bankroll -= bet
                    self.streak = 0
                    return True
                print("Player hits.")
            elif choice in ['s', 'stand']:
                print("Player stands.")
                break
            else:
                print("Invalid option.")
        return player_bust

    def dealer_turn(self, dealer_hand):
        while dealer_hand.calculate_value() < 17:
            dealer_hand.add_card(self.deck.draw_card())
        dealer_hand.display()
        print(f"Dealer's hand value: {dealer_hand.calculate_value()}")

    def resolve_hands(self, player_hand, dealer_hand, bet):
        player_value = player_hand.calculate_value()
        dealer_value = dealer_hand.calculate_value()

        if dealer_value > 21 or player_value > dealer_value:
            print("Player wins!")
            winnings = bet
            if player_value == 21 and len(player_hand.cards) == 2:
                winnings *= self.BLACKJACK_PAYOUT
            self.bankroll += winnings
            self.streak += 1
            print(f"Winnings: ${winnings:.2f}")
        elif player_value < dealer_value:
            print("Dealer wins!")
            self.bankroll -= bet
            self.streak = 0
            print(f"Loses: ${bet:.2f}")
        else:
            print("Push. The hand is a tie.")
            print(f"Bet returned: ${bet:.2f}")

        if self.streak > self.max_streak:
            self.max_streak = self.streak

    def play(self):
        while self.bankroll > 0:
            print(f"Starting hand {self.hands_played + 1}.")
            bet = self.get_bet()
            if bet is None:  # Player chose to exit
                break
            player_hand, dealer_hand = self.initial_deal()

            # Display initial hands
            print("Player's hand:")
            player_hand.display()
            print(f"Player's hand value: {player_hand.calculate_value()}")
            print("Dealer's hand:")
            dealer_hand.display(hide_first_card=True)

            # Player's turn
            player_bust = self.player_turn(player_hand, bet)

            # Dealer's turn only if player hasn't busted
            if not player_bust:
                self.dealer_turn(dealer_hand)

            # Determine the outcome
            if not player_bust:
                self.resolve_hands(player_hand, dealer_hand, bet)

            # Update the number of hands played after the hand is resolved
            self.hands_played += 1

            # Print bankroll, streak information, and cards left
            print(f"Current bankroll: ${self.bankroll:.2f}")
            print(f"Current winning streak: {self.streak}")
            print(f"Maximum winning streak: {self.max_streak}")
            print(f"Cards left in the deck: {self.deck.cards_left()}")

            # If all cards are dealt, reshuffle the deck
            if self.deck.cards_left() == 0:
                print("Reshuffling the deck.")
                self.deck = Deck(self.num_decks)

# Run the game
if __name__ == '__main__':
    game = Game()
    game.play()
