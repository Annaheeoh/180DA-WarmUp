import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/test/team6/#", qos=1)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    acceleration_x = payload.get('acceleration', {}).get('x')
    acceleration_y = payload.get('acceleration', {}).get('y')
    acceleration_z = payload.get('acceleration', {}).get('z')

    if acceleration_x is not None and acceleration_y is not None and acceleration_z is not None:
        print(f"Acceleration - X: {acceleration_x}, Y: {acceleration_y}, Z: {acceleration_z}")
    else:
        print("Incomplete acceleration data received")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)

client.loop_forever()
