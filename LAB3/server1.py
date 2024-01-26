import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Player 1 connected with result code " + str(rc))
    client.subscribe("ece180d/test/team6/player1", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Player 1: Unexpected Disconnect')
    else:
        print('Player 1: Expected Disconnect')

def on_message(client, userdata, message):
    time.sleep(1)
    received_choice = message.payload.decode()
    print('Player 1 received opponent\'s choice: ' + received_choice)
    play_game(int(received_choice))

def play_game(opponent_choice):
    # Implement your game logic here
    player1_choice = 1  # Assuming 1 represents Rock (you can modify accordingly)
    
    # Determine the winner
    if player1_choice == opponent_choice:
        result = 'draw'
    elif (player1_choice == 1 and opponent_choice == 3) or \
         (player1_choice == 2 and opponent_choice == 1) or \
         (player1_choice == 3 and opponent_choice == 2):
        result = 'win'
    else:
        result = 'lose'

    print('Player 1 result: ' + result)

    # Send the result to Player 2
    client.publish("ece180d/test/team6/player2", result, qos=1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

# Player 1 makes an initial choice (e.g., Rock)
initial_choice = 1
client.publish("ece180d/test/team6/player1", str(initial_choice), qos=1)

while True:
    pass

