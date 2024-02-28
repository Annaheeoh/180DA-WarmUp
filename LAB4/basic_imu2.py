#include <PubSubClient.h>
#include "arduino_secrets.h"
#include "ICM_20948.h"

// Uncomment this to use SPI
//#define USE_SPI

#define SERIAL_PORT Serial

#ifdef USE_SPI
    #define SPI_PORT SPI
    #define CS_PIN 2
#else
    #define WIRE_PORT Wire
    #define AD0_VAL 1
#endif

// WiFi credentials
const char *ssid = SECRET_SSID;
const char *password = SECRET_PASS;

// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";
const char *topic = "ece180d/test";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

#ifdef USE_SPI
    ICM_20948_SPI myICM;
#else
    ICM_20948_I2C myICM;
#endif

void setup() {
    Serial.begin(115200);

    // Connecting to WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the WiFi network");

    // Connecting to MQTT broker
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    while (!client.connected()) {
        String client_id = "esp32-client-";
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
        if (client.connect(client_id.c_str())) {
            Serial.println("mqtt broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }

    // Publish and subscribe
    client.publish(topic, "Hi I’m ESP32 ^^");
    client.subscribe(topic);

#ifdef USE_SPI
    SPI_PORT.begin();
#else
    WIRE_PORT.begin();
    WIRE_PORT.setClock(400000);
#endif

    // Initializing the sensor
    bool initialized = false;
    while (!initialized) {
#ifdef USE_SPI
        myICM.begin(CS_PIN, SPI_PORT);
#else
        myICM.begin(WIRE_PORT, AD0_VAL);
#endif

        SERIAL_PORT.print(F("Initialization of the sensor returned: "));
        SERIAL_PORT.println(myICM.statusString());
        if (myICM.status != ICM_20948_Stat_Ok) {
            SERIAL_PORT.println("Trying again...");
            delay(500);
        } else {
            initialized = true;
        }
    }
}

void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    if (myICM.dataReady()) {
        myICM.getAGMT();
        printScaledAGMT(&myICM);
        client.loop();
        delay(30);
    } else {
        SERIAL_PORT.println("Waiting for data");
        client.loop();
        delay(500);
    }
}

void printScaledAGMT(ICM_20948 *sensor) {
    SERIAL_PORT.print("Scaled. Acc (mg) [ ");
    printFormattedFloat(sensor->accX(), 5, 2);
    char buf[10];
    snprintf(buf, 10, "%f", sensor->accX());
    client.publish(topic, buf);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->accY(), 5, 2);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->accZ(), 5, 2);
    SERIAL_PORT.print(" ], Gyr (DPS) [ ");
    printFormattedFloat(sensor->gyrX(), 5, 2);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->gyrY(), 5, 2);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->gyrZ(), 5, 2);
    SERIAL_PORT.print(" ], Mag (uT) [ ");
    printFormattedFloat(sensor->magX(), 5, 2);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->magY(), 5, 2);
    SERIAL_PORT.print(", ");
    printFormattedFloat(sensor->magZ(), 5, 2);
    SERIAL_PORT.print(" ], Tmp (C) [ ");
    printFormattedFloat(sensor->temp(), 5, 2);
    SERIAL_PORT.print(" ]");
    SERIAL_PORT.println();
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals) {
    float aval = abs(val);
    if (val < 0) {
        SERIAL_PORT.print("-");
    } else {
        SERIAL_PORT.print(" ");
    }
    for (uint8_t indi = 0; indi < leading; indi++) {
        uint32_t tenpow = 0;
        if (indi < (leading - 1)) {
            tenpow = 1;
        }
        for (uint8_t c = 0; c < (leading - 1 - indi); c++) {
            tenpow *= 10;
        }
        if (aval < tenpow) {
            SERIAL_PORT.print("0");
        } else {
            break;
        }
    }
    if (val < 0) {
        SERIAL_PORT.print(-val, decimals);
    } else {
        SERIAL_PORT.print(val, decimals);
    }
}