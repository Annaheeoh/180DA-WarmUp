import paho.mqtt.client as mqtt
import random

# Global variable to store the player's choice
player_choice = None

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("rps/game/#")  # Subscribe to the topic for game communication

def on_message(client, userdata, message):
    topic = message.topic.split('/')[-1]
    if topic != "player_choice1":

        global player_choice
        opponent_choice = message.payload.decode()
        print('Opponent chose:', opponent_choice)
        result = determine_winner(player_choice, opponent_choice)
        print("Result:", result)

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.loop_start()

# Rock-Paper-Scissors Game Logic
choices = ['rock', 'paper', 'scissors']

def get_player_choice():
    global player_choice
    choice = input("Enter rock, paper, or scissors: ")
    while choice not in choices:
        choice = input("Invalid choice. Enter rock, paper, or scissors: ")
    player_choice = choice
    return choice

def determine_winner(user_choice, opponent_choice):
    if user_choice == opponent_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and opponent_choice == "scissors") or \
         (user_choice == "paper" and opponent_choice == "rock") or \
         (user_choice == "scissors" and opponent_choice == "paper"):
        return "You win!"
    else:
        return "You lose!"

# Main Game Loop
while True:
    player_choice = get_player_choice()
    client.publish("rps/game/player_choice1", player_choice)

client.loop_stop()
client.disconnect()
