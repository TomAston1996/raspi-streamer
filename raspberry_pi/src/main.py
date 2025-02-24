"""
App entry point
Author: Tom Aston
"""

from mqtt_client import MQTTClient
from cpu_metric import publish_cpu_metrics


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
