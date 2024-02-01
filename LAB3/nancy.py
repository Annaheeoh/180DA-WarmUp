import paho.mqtt.client as mqtt

# MQTT broker address and port
mqtt_broker = "localhost"
mqtt_port = 1883

# Define topics
topic_play = "game/play"
topic_result = "game/result"

# Client ID
client_id = input("Please enter your username: ")

# Define callback function to handle messages
def on_message(client, userdata, message):
    if message.topic == topic_play:
        opponent_choice = message.payload.decode()
        player_choice = input("Please enter your choice (rock/paper/scissors): ")
        # Determine the winner
        result = determine_winner(player_choice, opponent_choice)
        # Publish the result
        client.publish(topic_result, result)

def determine_winner(player_choice, opponent_choice):
    if player_choice == opponent_choice:
        return "It's a tie!"
    elif (player_choice == "rock" and opponent_choice == "scissors") or \
         (player_choice == "scissors" and opponent_choice == "paper") or \
         (player_choice == "paper" and opponent_choice == "rock"):
        return "You win!"
    else:
        return "You lose!"

# Initialize MQTT client
client = mqtt.Client(client_id)

# Set up the callback function
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port)

# Subscribe to the game topic
client.subscribe(topic_play)

# Start the loop to maintain connection
client.loop_forever()
