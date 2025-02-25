"""
Test suite for the MQTT client
Author: Tom Aston
"""

import json

from ..src.config import config_manager
from ..src.mqtt_client import MQTTClient


class TestSuiteMQTTClient:
    """
    Test suite for the MQTT client
    """

    def test_publish(self, mock_mqtt_client: MQTTClient) -> None:
        """Test if publish method correctly sends a message."""
        topic = "test/topic"
        payload = "test payload"
        mock_mqtt_client.publish(topic, payload)
        expected_payload = json.dumps(payload)

        mock_mqtt_client.client.publish.assert_called_once_with(
            topic=topic, payload=expected_payload, qos=0, retain=False
        )

    def test_connect(self, mock_mqtt_client: MQTTClient) -> None:
        """Test if connect method correctly connects to the broker."""
        mock_mqtt_client.connect()
        mock_mqtt_client.client.connect.assert_called_once_with(
            host=config_manager.RPI_AWS_IOT_ENDPOINT, port=8883, keepalive=60
        )
