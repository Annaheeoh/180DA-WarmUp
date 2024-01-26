import paho.mqtt.client as mqtt

# Define callbacks - functions that run when events happen.

# Publisher Callbacks
def on_publish(client, userdata, mid):
    print("Message Published")

# Subscriber Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("ece180d/test/team6/4", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

# Create a client instance.
client = mqtt.Client()

# Add additional client options (security, certifications, etc.)
# Many default options should be good to start off.

# Check if running as a publisher or subscriber
mode = input("Enter 'p' for publisher, 's' for subscriber: ")

if mode == 'p':
    # Publisher setup
    client.on_publish = on_publish
    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    # Publishing a message
    print('Publishing...')
    for i in range(1):
        client.publish("ece180d/test/team6", "Hello, I'm anna", qos=1)

    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()

elif mode == 's':
    # Subscriber setup
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    # Keep the script running
    while True:
        pass

    # Stop the loop and disconnect (never reached in this example)
    client.loop_stop()
    client.disconnect()

else:
    print("Invalid mode. Enter 'p' for publisher or 's' for subscriber.")
