import random

def calculate_payout_multiplier(user_choice):
    # Calculate the payout multiplier as a function of how far the choice is from 50
    return 1 - (abs(50 - user_choice) / 50)

def cli_probability_game_with_betting():
    # Welcome message and initial deposit
    print("Welcome to the Probability Game with Betting!")
    print("You can start by making a deposit to set your initial balance.")

    while True:
        initial_deposit = input("Please enter your initial deposit (positive integer) or type 'exit', 'q', or 'quit' to leave: ").lower()
        if initial_deposit in ['exit', 'q', 'quit']:
            print("You have chosen to exit the game. Goodbye!")
            return
        try:
            user_coins = int(initial_deposit)
            if user_coins > 0:
                break
            else:
                print("Invalid deposit amount. The deposit must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid positive integer.")

    print(f"You have deposited {user_coins} playmoney coins.")
    
    while True:  # Run indefinitely until the user quits
        user_input = input("Enter your number (1-99), or type 'exit', 'q', or 'quit' to leave the game: ").lower()
        if user_input in ['exit', 'q', 'quit']:
            print(f"Your final balance is {user_coins} coins. Thank you for playing!")
            break

        try:
            user_choice = int(user_input)
        except ValueError:
            print("Please enter a valid integer or 'exit', 'q', 'quit' to leave the game.")
            continue

        if user_choice <= 0 or user_choice >= 100:
            print("Invalid number. Please choose a number between 1 and 99.")
            continue
        
        user_bet_choice = input("Do you bet over or under? (Type 'over' or 'under'): ").lower()
        if user_bet_choice not in ['over', 'under']:
            print("Invalid choice. Please type 'over' or 'under'.")
            continue
        
        bet_amount = input(f"How much do you want to bet? You have {user_coins} coins, or type 'exit', 'q', 'quit' to leave the game: ").lower()
        if bet_amount in ['exit', 'q', 'quit']:
            print(f"Your final balance is {user_coins} coins. Thank you for playing!")
            break

        try:
            bet_amount = int(bet_amount)
        except ValueError:
            print("Please enter a valid integer or 'exit', 'q', 'quit' to leave the game.")
            continue

        if bet_amount <= 0 or bet_amount > user_coins:
            print(f"Invalid bet amount. You can bet between 1 and {user_coins} coins.")
            continue
        
        machine_number = random.randint(1, 99)
        print(f"The machine generated the number: {machine_number}")
        
        payout_multiplier = calculate_payout_multiplier(user_choice)
        potential_payout = bet_amount * payout_multiplier

        if (user_bet_choice == 'under' and user_choice < machine_number) or (user_bet_choice == 'over' and user_choice > machine_number):
            user_coins += potential_payout
            print(f"Congratulations! You win! Your payout multiplier is {payout_multiplier:.2f}, and your payout is {potential_payout:.2f} coins. You now have {user_coins:.2f} coins.")
        elif user_choice == machine_number:
            # Bonus for guessing the exact number remains constant
            user_coins += 10 * bet_amount
            print(f"Incredible! You've guessed the exact number. You get a bonus and now have {user_coins} coins!")
        else:
            user_coins -= bet_amount
            print(f"Sorry, you lose this round. Your payout multiplier was {payout_multiplier:.2f}. You now have {user_coins} coins.")
        
        if user_coins <= 0:
            print("You've run out of coins! Game over.")
            break

if __name__ == "__main__":
    cli_probability_game_with_betting()
