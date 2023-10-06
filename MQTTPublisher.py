import paho.mqtt.client as mqtt
from paho import mqtt as paho
import time
from ruamel.yaml import YAML


class MQTTPublisher:
    def __init__(self, config_path):
        # Load MQTT configuration from YAML file
        self.config = self._load_config(config_path)
        self.client = mqtt.Client(protocol=mqtt.MQTTv5)

        # enable TLS for secure connection
        self.client.tls_set(tls_version=paho.client.ssl.PROTOCOL_TLS)

        # Setup username and password if provided
        if self.config.get("username") and self.config.get("password"):
            self.client.username_pw_set(
                self.config["username"], self.config["password"]
            )

    def _load_config(self, config_path):
        yaml = YAML()
        with open(config_path, "r") as file:
            config = yaml.load(file)
        return config["MQTT"]

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {str(rc)}")

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_disconnect(self, client, userdata, rc, properties=None):
        print(f"Disconnected with result code {str(rc)}")

    def connect(self):
        # Set callback functions
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

        # Connect to the broker
        self.client.connect(self.config["server"], int(self.config["port"]), 60)

    def publish(self, topic, message):
        # Publish a message to a topic
        self.client.publish(topic, message, qos=1)


# Usage Example
if __name__ == "__main__":
    publisher = MQTTPublisher("config.yaml")

    try:
        publisher.connect()
        publisher.publish(
            publisher.config["topic"], "Test warning message"
        )  # Publish a test message
        publisher.client.loop_start()  # Let the client loop for a short period to handle potential callbacks
        time.sleep(2)  # Wait to ensure message is sent before disconnecting
    finally:
        publisher.client.loop_stop()
        publisher.client.disconnect()
