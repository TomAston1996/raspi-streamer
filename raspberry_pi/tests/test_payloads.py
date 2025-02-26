"""
Test suite for payloads
Author: Tom Aston
"""

import pytest

from ..src.payloads import CPUMetricPayload


class TestSuitCPUMetricPayload:
    """
    Test suite for CPU metric payload
    """

    @pytest.fixture
    def valid_payload(self) -> CPUMetricPayload:
        """fixture for valid payload"""
        return {
            "cpu_usage": 45,
            "timestamp": 1700000000.123,
            "device": "raspberry_pi_4",
            "location": "office",
            "unit": "%",
            "topic": "cpu_metrics",
            "loop_count": 10,
            "project": "iot-monitoring",
            "version": "1.0.0",
        }

    def test_valid_payload(self, valid_payload: CPUMetricPayload) -> None:
        """test for valid payload

        Args:
            valid_payload (CPUMetricPayload): cpu metric payload dictionary
        """
        assert set(valid_payload.keys()) == {
            "cpu_usage", "timestamp", "device", "location", "unit",
            "topic", "loop_count", "project", "version"
        }
        assert isinstance(valid_payload["cpu_usage"], int)
        assert isinstance(valid_payload["timestamp"], float)
        assert isinstance(valid_payload["device"], str)
        assert isinstance(valid_payload["location"], str)
        assert isinstance(valid_payload["unit"], str)
        assert isinstance(valid_payload["topic"], str)
        assert isinstance(valid_payload["loop_count"], int)
        assert isinstance(valid_payload["project"], str)
        assert isinstance(valid_payload["version"], str)
