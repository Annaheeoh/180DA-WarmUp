import random

class RockPaperScissorsBot:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.results = {'win': 0, 'lose': 0, 'draw': 0}

    def get_user_choice(self):
        user_choice = input("Enter your choice (rock/paper/scissors): ").lower()
        while user_choice not in self.choices:
            print("Invalid choice. Please enter rock, paper, or scissors.")
            user_choice = input("Enter your choice (rock/paper/scissors): ").lower()
        return user_choice

    def generate_bot_choice(self):
        return random.choice(self.choices)

    def determine_winner(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return 'draw'
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            return 'win'
        else:
            return 'lose'

    def play_game(self):
        while True:
            user_choice = self.get_user_choice()
            bot_choice = self.generate_bot_choice()

            print(f"You chose: {user_choice}")
            print(f"Bot chose: {bot_choice}")

            result = self.determine_winner(user_choice, bot_choice)
            self.results[result] += 1

            print(f"Result: {result.capitalize()}!\n")
            print("Game Results:")
            print(f"Wins: {self.results['win']}, Losses: {self.results['lose']}, Draws: {self.results['draw']}\n")

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != 'yes':
                break

if __name__ == "__main__":
    rps_bot = RockPaperScissorsBot()
    rps_bot.play_game()

