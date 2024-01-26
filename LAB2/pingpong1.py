import paho.mqtt.client as mqtt
import time
import numpy as np
# Define callbacks - functions that run when events happen.

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/team6/#", qos=1)
    #client.publish("ece180d/test/team6/2","hi" , qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (won't be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    time.sleep(1)
    topic = int(message.topic.split('/')[-1])
    if topic != 2:
        print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))
        num = int((message.payload)) +1
        client.publish("ece180d/test/team6/2", num, qos=1)
        print("sent message: " + str(num))

# 1. Create a client instance.
client = mqtt.Client()

# Add additional client options (security, certifications, etc.)
# Many default options should be good to start off.
# Add callbacks to the client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. Connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')

# 3. Call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

# 4. Use subscribe() to subscribe to a topic and receive messages.
while True:
    pass
# Use publish() to publish messages to the broker.
# Payload must be a string, bytearray, int, float, or None.

# Use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()
