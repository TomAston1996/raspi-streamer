"""
Module to get cpu metrics
Author: Tom Aston
"""

import random
import time

from config import config_manager
from mqtt_client import MQTTClient
from payloads import CPUMetricPayload

TOPIC = "device/cpu"


def publish_cpu_metrics(client: MQTTClient, loop_count: int = 10) -> None:
    """Publish CPU metrics to the MQTT broker.

    Args:
        client (MQTTClient): mqtt client
        loop_count (int): how many times to loop
    """
    while loop_count > 0:
        cpu_usage = random.randint(0, 100)

        # TODO replace mock data with actual CPU usage
        message_payload = CPUMetricPayload(
            cpu_usage=cpu_usage,
            timestamp=time.time(),
            device="Raspberry Pi",
            location="Home",
            unit="percentage",
            topic=TOPIC,
            loop_count=loop_count,
            project=config_manager.PROJECT_NAME,
            version=config_manager.VERSION,
        )

        client.publish(topic=TOPIC, payload=message_payload)

        print(f"Published CPU Usage: {cpu_usage} to topic: {TOPIC}")
        time.sleep(5)
        loop_count -= 1
