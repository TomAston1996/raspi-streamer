"""
Test suite for the CPU metric.
Author: Tom Aston
"""

from ..src.cpu_metric import publish_cpu_metrics
from ..src.mqtt_client import MQTTClient


class TestSuiteCPUMetrics:
    """
    Test suite for the CPU metric.
    """

    def test_publish_cpu_metrics(self, mock_mqtt_client: MQTTClient) -> None:
        """
        Test if CPU metrics are published correctly.
        """
        publish_cpu_metrics(mock_mqtt_client, 1)
        assert mock_mqtt_client.client.publish.call_count == 1
        assert mock_mqtt_client.client.publish.called_with(topic="device/cpu")
