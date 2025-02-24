"""
App entry point
Author: Tom Aston
"""

from cpu_metric import publish_cpu_metrics
from mqtt_client import MQTTClient


def main() -> None:
    """
    Main function
    """
    print("Starting Raspberry Pi IoT")
    mqtt_client = MQTTClient()
    mqtt_client.connect()
    mqtt_client.start()
    publish_cpu_metrics(mqtt_client, 5)
    mqtt_client.stop()


if __name__ == "__main__":
    main()
