"""
Service module for CPU metrics
Author: Tom Aston
"""

from typing import List

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import CpuMetricSchema


class CpuMetricsService:
    """
    CPU Metrics Service
    """

    def get_all_cpu_metrics(self, cpu_metric_table: Table) -> List[CpuMetricSchema]:
        """
        Get all CPU metrics
        """
        all_cpu_metrics = []

        # scan for all items in the table where the timestamp is greater than 0 (all items with a timestamp)
        scan_kwargs = {
            "FilterExpression": Key("timestamp").gt(0),
            "ProjectionExpression": "#timestamp, #cpu_usage, #device, #location, #unit, #topic, #loop_count, #project, #version",
            "ExpressionAttributeNames": {
                "#timestamp": "timestamp",
                "#cpu_usage": "cpu_usage",
                "#device": "device",
                "#location": "location",
                "#unit": "unit",
                "#topic": "topic",
                "#loop_count": "loop_count",
                "#project": "project",
                "#version": "version",
            },
        }

        done = False
        start_key = None
        try:
            while not done:
                if start_key:
                    scan_kwargs["ExclusiveStartKey"] = start_key
                response = cpu_metric_table.scan(**scan_kwargs)
                all_cpu_metrics.extend(response.get("Items", []))
                start_key = response.get("LastEvaluatedKey", None)
                done = start_key is None

            return all_cpu_metrics
        except ClientError as err:
            print(f"ClientError: {err}")
            raise RuntimeError("Error getting all CPU metrics") from err
