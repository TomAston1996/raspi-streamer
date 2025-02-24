"""
This file is used to create a MQTT client that will be used to send data to the MQTT broker.
Author: Tom Aston
"""

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import ssl
from typing import Any
import json

from config import config_manager
from payloads import CPUMetricPayload


class MQTTClient:
    """
    MQTT Client
    """

    def __init__(self) -> None:
        """Initialize the MQTT Client."""
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect

        # Configure TLS for AWS IoT Core
        self.client.tls_set(
            ca_certs=config_manager.RPI_AWS_IOT_ROOT_CA,
            certfile=config_manager.RPI_AWS_IOT_CERTIFICATE,
            keyfile=config_manager.RPI_AWS_IOT_PRIVATE_KEY,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )

        self.client.tls_insecure_set(
            True
        )  # AWS IoT does not provide a broker certificate

    def __on_connect(self, client: Client, userdata: Any, flags: dict, rc: int) -> None:
        """Callback function for when the client receives a CONNACK response from the server.

        Args:
            client (Client): mqtt client
            userdata (Any): user data
            flags (dict): flags
            rc (int): result code
        """
        print(f"Connected to MQTT Broker with result code {rc}")

    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(
            host=config_manager.RPI_AWS_IOT_ENDPOINT,
            port=8883,
            keepalive=60,
        )

    def loop_forever(self) -> None:
        """Start the MQTT loop forever."""
        self.client.loop_forever()

    def start(self) -> None:
        """Start the MQTT loop."""
        self.client.loop_start()

    def publish(self, topic: str, payload: str | CPUMetricPayload) -> None:
        """publish a message to a topic.

        Args:
            topic (str): topic to publish to
            payload (str | dict[Any, Any]): message to publish
        """
        try:
            payload = json.dumps(payload)
            self.client.publish(topic=topic, payload=payload, qos=0, retain=False)
        except ValueError:
            print("Error publishing message")

    def stop(self) -> None:
        """Stop the MQTT loop."""
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT Broker")
