"""
Global fixtures for pytest
Author: Tom Aston
"""

from unittest.mock import Mock

import pytest

from ..src.mqtt_client import MQTTClient


@pytest.fixture
def mock_mqtt_client():
    """Fixture to create a mock MQTTClient instance."""
    client = MQTTClient()
    client.client = Mock()
    return client
