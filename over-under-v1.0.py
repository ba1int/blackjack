import random

def cli_probability_game_with_betting():
    # Initialize user's playmoney coins
    user_coins = 100  # Starting with 100 playmoney coins
    
    # Starting the game with a welcome message
    print("Welcome to the Probability Game with Betting!")
    print("You start with 100 playmoney coins.")
    print("Pick a number between 0 and 100 and guess if your number will be over or under the number the machine generates.")
    print("If you guess correctly, you win double your bet. Guess the exact number for a bonus of ten times your bet!")
    
    while user_coins > 0:
        # User inputs their choice
        try:
            user_choice = int(input("Enter your number (0-100): "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if user_choice < 0 or user_choice > 100:
            print("Invalid number. Please choose a number between 0 and 100.")
            continue
        
        # User inputs their bet
        user_bet_choice = input("Do you bet over or under? (Type 'over' or 'under'): ").lower()
        if user_bet_choice not in ['over', 'under']:
            print("Invalid choice. Please type 'over' or 'under'.")
            continue
        
        # User inputs their bet amount
        try:
            bet_amount = int(input(f"How much do you want to bet? You have {user_coins} coins: "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if bet_amount <= 0 or bet_amount > user_coins:
            print(f"Invalid bet amount. You can bet between 1 and {user_coins} coins.")
            continue
        
        # Game logic
        machine_number = random.randint(0, 100)
        print(f"The machine generated the number: {machine_number}")
        
        # Determine the result and update coins
        if user_bet_choice == 'under' and user_choice < machine_number:
            user_coins += bet_amount
            print(f"Congratulations! You win! You now have {user_coins} coins.")
        elif user_bet_choice == 'over' and user_choice > machine_number:
            user_coins += bet_amount
            print(f"Congratulations! You win! You now have {user_coins} coins.")
        elif user_choice == machine_number:
            user_coins += 10 * bet_amount
            print(f"Incredible! You've guessed the exact number. You get a bonus and now have {user_coins} coins!")
        else:
            user_coins -= bet_amount
            print(f"Sorry, you lose this round. You now have {user_coins} coins.")
        
        # Check if user still has coins to play
        if user_coins <= 0:
            print("You've run out of coins! Game over.")
            break
        
        # Option to play again
        play_again = input("Would you like to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thank you for playing the Probability Game with Betting. Goodbye!")
            break

# The game will start immediately when the program is called
if __name__ == "__main__":
    cli_probability_game_with_betting()