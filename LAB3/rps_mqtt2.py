import pygame
import paho.mqtt.client as mqtt
import sys
import os

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 780, 600
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")
font = pygame.font.Font(None, 36)

# Load Images
def load_image(name):
    path = os.path.join(os.getcwd(), f"{name}.jpg")
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (120, 120))

class RockPaperScissorsGame:
    def __init__(self):
        self.rock = load_image("rock")
        self.paper = load_image("paper")
        self.scissors = load_image("scissors")
        self.wins = 0
        self.losses = 0
        self.opponent_choice = None
        self.client = mqtt.Client()
        self.setup_mqtt()

    def setup_mqtt(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async('mqtt.eclipseprojects.io')
        self.client.loop_start()

    def on_message(self, client, userdata, message):
        self.opponent_choice = message.payload.decode()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe('rps/game/player1', qos=1)

    def write_text(self, text, colour, x, y):
        text_surface = font.render(text, True, colour)
        screen.blit(text_surface, (x, y))

    def draw_button(self, text, button_colour, text_colour, x, y, width, height):
        button = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, button_colour, button)
        self.write_text(text, text_colour, x, y)

    def get_player_choice(self):
        screen.fill(WHITE)
        self.write_text("Choose rock, paper, or scissors", RED, 220, 50)
        screen.blit(self.rock, (140, 240))
        screen.blit(self.paper, (340, 240))
        screen.blit(self.scissors, (540, 240))
        pygame.display.flip()
        return self.handle_choice()

    def handle_choice(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return self.process_mouse_click(event.pos)

    def process_mouse_click(self, pos):
        x, y = pos
        if 140 <= x <= 260 and 240 <= y <= 360:
            return "rock"
        elif 340 <= x <= 460 and 240 <= y <= 360:
            return "paper"
        elif 540 <= x <= 660 and 240 <= y <= 360:
            return "scissors"

    def determine_winner(self, player_choice):
        if player_choice == self.opponent_choice:
            return "It's a tie!"
        elif (player_choice == "rock" and self.opponent_choice == "scissors") or \
             (player_choice == "paper" and self.opponent_choice == "rock") or \
             (player_choice == "scissors" and self.opponent_choice == "paper"):
            self.wins += 1
            return "You win! Opponent chose " + self.opponent_choice
        else:
            self.losses += 1
            return "You lose! Opponent chose " + self.opponent_choice

    def game_loop(self):
        player_choice = self.get_player_choice()
        self.client.publish('rps/game/player2', player_choice)

        while self.opponent_choice is None: 
            screen.fill(WHITE)
            self.write_text("Waiting for opponent...", BLACK, 220, 300)
            pygame.display.flip()

        result = self.determine_winner(player_choice)
        screen.fill(WHITE)
        self.write_text(f"You chose {player_choice}.", BLACK, 100, 100)
        self.write_text(f"Opponent chose {self.opponent_choice}.", BLACK, 100, 200)
        self.write_text(result, BLACK, 100, 300)
        self.write_text(f"Wins: {self.wins}.", BLACK, 100, 400)
        self.write_text(f"Losses: {self.losses}.", BLACK, 300, 400)
        self.draw_button("Quit", BLACK, WHITE, 100, 500, 100, 50)
        self.draw_button("Play Again", BLACK, WHITE, 500, 500, 200, 50)
        pygame.display.flip()  
        return self.check_for_quit_or_play_again()

    def check_for_quit_or_play_again(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 100 <= x <= 200 and 500 <= y <= 550:
                        pygame.quit()
                        sys.exit()
                    elif 500 <= x <= 700 and 500 <= y <= 550:
                        self.opponent_choice = None
                        return True

def main():
    game = RockPaperScissorsGame()
    while game.game_loop():
        continue

if __name__ == "__main__":
    main()
