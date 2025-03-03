"""
Service module for CPU metrics
Author: Tom Aston

Resource
--------
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/query.html
"""

from typing import List, Optional

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table

from ..errors import InvalidRequestException, ServerException
from .schemas import CpuMetricSchema


class CpuMetricsService:
    """
    CPU Metrics Service
    """

    def get_cpu_metrics(
        self, cpu_metric_table: Table, key: str = None, value: int | str = None, operator: str = None
    ) -> List[CpuMetricSchema]:
        """
        Get CPU metrics
        """
        if key and value and operator:
            return self._get_filtered_cpu_metrics(cpu_metric_table, key, value, operator)
        else:
            return self._get_all_cpu_metrics(cpu_metric_table)

    def _get_all_cpu_metrics(self, cpu_metric_table: Table) -> List[CpuMetricSchema]:
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

    def _get_filtered_cpu_metrics(
        self, cpu_metric_table: Table, key: str, value: int | str, operator: str
    ) -> List[CpuMetricSchema]:
        """
        Get a CPU metric
        """
        if operator not in {"eq", "gt", "lt"}:
            raise InvalidRequestException()

        try:
            # TODO make this dynamic based on the key, value and operator
            response = cpu_metric_table.query(
                IndexName="TimestampCpuUsageIndex",  # Use the GSI name
                KeyConditionExpression=Key("cpu_usage").eq(52),  # Filtering by CPU usage
            )

            return response.get("Items", [])
        except ClientError as err:
            print(f"ClientError: {err}")
            raise ServerException()
