"""
Global fixtures for pytest
Author: Tom Aston
"""

from unittest.mock import Mock, patch

import pytest

from ..src.mqtt_client import MQTTClient


@pytest.fixture
def mock_mqtt_client() -> MQTTClient:
    """Fixture to create a mock MQTTClient instance."""
    with patch("paho.mqtt.client.Client.tls_set", return_value=None), \
        patch("paho.mqtt.client.Client.tls_insecure_set", return_value=None):
        client = MQTTClient()
        client.client = Mock()  # Mock MQTT client object
    
    return client
