import paho.mqtt.client as mqtt
import numpy as np

# Define callbacks - functions that run when events happen.

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect, then subscriptions will be renewed.
    # client.subscribe("ece180d/test")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (won't be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

# Create a client instance.
client = mqtt.Client()

# Add additional client options (security, certifications, etc.)
# Many default options should be good to start off.

# Add callbacks to the client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')

# Call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# Use subscribe() to subscribe to a topic and receive messages.

# Use publish() to publish messages to the broker.
# Payload must be a string, bytearray, int, float, or None.
print('Publishing...')
for i in range(1):
    client.publish("ece180d/test/team6", "Hello, I'm anna", qos=1)

# Use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
