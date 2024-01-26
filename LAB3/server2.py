import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Player 2 connected with result code " + str(rc))
    client.subscribe("ece180d/test/team6/player2", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Player 2: Unexpected Disconnect')
    else:
        print('Player 2: Expected Disconnect')

def on_message(client, userdata, message):
    time.sleep(1)
    received_result = message.payload.decode()
    print('Player 2 received result: ' + received_result)
    play_game()

def play_game():
    # Implement your game logic here
    player2_choice = 2  # Assuming 2 represents Paper (you can modify accordingly)
    
    # Send the choice to Player 1
    client.publish("ece180d/test/team6/player1", str(player2_choice), qos=1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('mqtt.eclipseprojects.io')
client.loop_start()

while True:
    pass
