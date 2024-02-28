import pygame
import paho.mqtt.client as mqtt
import sys
import os

global opponent_choice
global wins
global losses

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock, Paper, Scissors")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

rock = pygame.image.load(os.path.join(os.getcwd(), r"rock.png"))
paper = pygame.image.load(os.path.join(os.getcwd(), r"paper.png"))
scissors = pygame.image.load(os.path.join(os.getcwd(), r"scissors.png"))
   
rock = pygame.transform.scale(rock, (120, 120))
paper = pygame.transform.scale(paper, (120, 120))
scissors = pygame.transform.scale(scissors, (120, 120))

choices = ['rock', 'paper', 'scissors']

wins = 0
losses = 0
opponent_choice = None
client = mqtt.Client()

# Function to handle receiving opponent's choice
def on_message(client, userdata, message):
    global opponent_choice
    opponent_choice = message.payload.decode()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('rps/game/player1', qos=1)

def write_text(text, colour, x, y):
    text_surface = font.render(text, True, colour)
    screen.blit(text_surface, (x, y))

def draw_button(text, button_colour, text_colour, x, y, width, height):
    button = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_colour, button)
    write_text(text, text_colour, x, y)

def get_player_choice():
    screen.fill(WHITE)
    write_text("Choose rock, paper, or scissors", RED, 220, 50)
    screen.blit(rock, (140, 240))
    screen.blit(paper, (340, 240))
    screen.blit(scissors, (540, 240))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 140 <= x <= 260 and 240 <= y <= 360:
                    print("rock")
                    return "rock"
                elif 340 <= x <= 460 and 240 <= y <= 360:
                    print("paper")
                    return "paper"
                elif 540 <= x <= 660 and 240 <= y <= 360:
                    print("scissors")
                    return "scissors"

def determine_winner(player_choice, opponent_choice):
    global wins 
    global losses
    if player_choice == opponent_choice:
        return "It's a tie!"
    elif (player_choice == "rock" and opponent_choice == "scissors") or \
         (player_choice == "paper" and opponent_choice == "rock") or \
         (player_choice == "scissors" and opponent_choice == "paper"):
        wins += 1
        return "You win! Opponent chose " + opponent_choice
    else:
        losses += 1
        return "You lose! Opponent chose " + opponent_choice

# Main game loop
def main():
    global opponent_choice
    global wins
    global losses

    client.on_connect = on_connect 
    client.on_message = on_message
    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    while True:

        player_choice = get_player_choice()
        client.publish('rps/game/player2', player_choice)

        while opponent_choice is None: 
            screen.fill(WHITE)
            write_text("Waiting for opponent...", BLACK, 220, 300)
            pygame.display.flip()

        pygame.display.flip()
        screen.fill(WHITE)
        result = determine_winner(player_choice, opponent_choice)
        write_text(f"You chose {player_choice}.", BLACK, 100, 100)
        write_text(f"Opponent chose {opponent_choice}.", BLACK, 100, 200)
        write_text(result, BLACK, 100, 300)
        write_text(f"Wins: {wins}.", BLACK, 100, 400)
        write_text(f"Losses: {losses}.", BLACK, 300, 400)
        draw_button("Quit", BLACK, WHITE, 100, 500, 100, 50)
        draw_button("Play Again", BLACK, WHITE, 500, 500, 200, 50)
        pygame.display.flip()  

        while True:
            again = 0
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
                        again = 1
                        break
            if again == 1:
                break
        pygame.display.flip()

        opponent_choice = None

if __name__ == "__main__":
    main()