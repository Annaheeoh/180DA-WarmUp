# player1_pygame.py
import pygame
import sys
import paho.mqtt.client as mqtt
import subprocess

pygame.init()

WIDTH, HEIGHT = 400, 300
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

USER_SCORE = 0
COMP_SCORE = 0
USER_CHOICE = ""
COMP_CHOICE = ""

# MQTT Setup
broker_address = "mqtt.eclipseprojects.io"
client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.loop_start()

def choice_to_number(choice):
    rps = {'rock': 0, 'paper': 1, 'scissor': 2}
    return rps[choice]

def number_to_choice(number):
    rps = {0: 'rock', 1: 'paper', 2: 'scissor'}
    return rps[number]

def random_computer_choice():
    return random.choice(['rock', 'paper', 'scissor'])

def on_message(client, userdata, message):
    global USER_CHOICE, COMP_CHOICE, USER_SCORE, COMP_SCORE

    if message.topic == "rps/game/player2_choice":
        comp_choice = message.payload.decode()
        COMP_CHOICE = choice_to_number(comp_choice)
    elif message.topic == "rps/game/result":
        result_data = message.payload.decode().split(",")
        USER_SCORE, COMP_SCORE = map(int, result_data)
    
    USER_CHOICE = choice_to_number(USER_CHOICE)

    if USER_CHOICE == COMP_CHOICE:
        print("Tie")
    elif (USER_CHOICE - COMP_CHOICE) % 3 == 1:
        print("You win")
        USER_SCORE += 1
    else:
        print("Comp wins")
        COMP_SCORE += 1

    update_display()

def update_display():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Your Score: {USER_SCORE}   Computer Score: {COMP_SCORE}", True, BLACK)
    screen.blit(text, (50, 220))
    pygame.display.flip()

# MQTT Callbacks
client.on_message = on_message
client.subscribe("rps/game/player2_choice")
client.subscribe("rps/game/result")

# Pygame setup
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rock Paper Scissors - Player 1")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    update_display()
