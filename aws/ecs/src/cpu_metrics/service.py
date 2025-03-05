"""
Service module for CPU metrics
Author: Tom Aston

Resource
--------
- https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
"""

import time
import uuid
from typing import List

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table

from ..errors import InvalidRequestException, ServerException
from .schemas import CpuMetricCreateSchema, CpuMetricQueryParams, CpuMetricSchema, CpuMetricUpdateSchema


class CpuMetricsService:
    """
    CPU Metrics Service
    """

    def get_cpu_metrics(self, cpu_metric_table: Table, params: CpuMetricQueryParams) -> List[CpuMetricSchema]:
        """router facing method to get cpu metrics based on the query parameters
        will return all cpu metrics if no query parameters are provided

        Args:
            cpu_metric_table (Table): cpu metric table
            params (CpuMetricQueryParams): query parameters including location, operator, and cpu usage value

        Returns:
            List[CpuMetricSchema]: list of cpu metrics data with all attributes included
        """
        if params.location_value and params.operator and params.cpu_usage_value is not None:
            return self._get_filtered_cpu_metrics(cpu_metric_table, params=params)
        else:
            return self._get_all_cpu_metrics(cpu_metric_table)

    def _get_all_cpu_metrics(self, cpu_metric_table: Table) -> List[CpuMetricSchema]:
        """scan for all items in the table where the timestamp is greater than 0 (all items with a timestamp)

        Args:
            cpu_metric_table (Table): cpu metric table

        Raises:
            ServerException: server error if the scan fails

        Returns:
            List[CpuMetricSchema]: list of cpu metrics data with all attributes included
        """
        all_cpu_metrics = []

        # scan for all items in the table where the timestamp is greater than 0 (all items with a timestamp)
        scan_kwargs = {
            "FilterExpression": Key("timestamp").gt(0),
            "ProjectionExpression": "#id, #timestamp, #cpu_usage, #device, #location, #unit, #topic, #loop_count, #project, #version",
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
                "#id": "id",
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
            raise ServerException()

    def _get_filtered_cpu_metrics(self, cpu_metric_table: Table, params: CpuMetricQueryParams) -> List[CpuMetricSchema]:
        """filters the cpu metrics based on the query parameters provided
        the use has to provide the location to be filtered by and the rnage is determined by the operator and cpu usage value

        Args:
            cpu_metric_table (Table): cpu metric table
            params (CpuMetricQueryParams): query parameters including location, operator, and cpu usage value

        Raises:
            InvalidRequestException: raised if the operator or location value is not valid
            ServerException: raised if the query fails

        Returns:
            List[CpuMetricSchema]: list of cpu metrics data with all attributes included
        """
        cpu_usage_value = int(params.cpu_usage_value)

        if params.location_value == "*":
            return self._get_all_devices_filtered_by_cpu_usage(cpu_metric_table, cpu_usage_value, params.operator)

        key_expressions = {
            "eq": Key("cpu_usage").eq(cpu_usage_value),
            "gt": Key("cpu_usage").gt(cpu_usage_value),
            "lt": Key("cpu_usage").lt(cpu_usage_value),
            "*": Key("cpu_usage").gt(0),  # all values
        }

        try:
            response = cpu_metric_table.query(
                IndexName="LocationIndex",  # Use the GSI name
                KeyConditionExpression=(Key("location").eq(params.location_value) & key_expressions[params.operator]),
            )
        except ClientError as err:
            print(f"ClientError: {err}")
            raise ServerException()
        else:
            return response.get("Items", [])

    def _get_all_devices_filtered_by_cpu_usage(
        self, cpu_metric_table: Table, cpu_usage: int, operator: str
    ) -> List[CpuMetricSchema]:
        """get all devices filtered by cpu usage

        Args:
            cpu_metric_table (Table): cpu metric table
            cpu_usage (int): cpu usage value
            operator (str): operator to filter by whch will be eq, gt, lt, or *

        Returns:
            List[CpuMetricSchema]: list of cpu metrics data with all attributes included
        """
        all_cpu_metrics = self._get_all_cpu_metrics(cpu_metric_table)

        if operator == "*":
            return all_cpu_metrics

        filter_operators = {
            "eq": lambda x: x == cpu_usage,
            "gt": lambda x: x > cpu_usage,
            "lt": lambda x: x < cpu_usage,
        }

        return [metric for metric in all_cpu_metrics if filter_operators[operator](metric["cpu_usage"])]

    def create_cpu_metric(self, cpu_metric_table: Table, cpu_metric: CpuMetricCreateSchema) -> CpuMetricSchema:
        """router facing method to create a cpu metric

        Args:
            cpu_metric_table (Table): cpu metric table
            cpu_metric (CpuMetricSchema): cpu metric data

        Returns:
            CpuMetricSchema: created cpu metric data
        """
        item_data = cpu_metric.model_dump()
        item_data["id"] = str(uuid.uuid4())
        item_data["timestamp"] = int(time.time())

        try:
            cpu_metric_table.put_item(Item=item_data)
        except ClientError as err:
            print(f"ClientError: {err}")
            raise ServerException()
        else:
            return item_data

    def batch_create_cpu_metrics(
        self, cpu_metric_table: Table, cpu_metrics: List[CpuMetricCreateSchema]
    ) -> List[CpuMetricSchema]:
        """router facing method to batch create cpu metrics

        Args:
            cpu_metric_table (Table): cpu metric table
            cpu_metrics (List[CpuMetricSchema]): list of cpu metric data

        Returns:
            List[CpuMetricSchema]: list of created cpu metric data
        """
        created_items: List[CpuMetricCreateSchema] = []
        with cpu_metric_table.batch_writer() as batch:
            for cpu_metric in cpu_metrics:
                item_data = cpu_metric.model_dump()
                item_data["id"] = str(uuid.uuid4())
                item_data["timestamp"] = int(time.time())
                created_items.append(item_data)
                batch.put_item(Item=item_data)

        return created_items

    def update_cpu_metric(self, cpu_metric_table: Table, cpu_metric: CpuMetricUpdateSchema) -> CpuMetricSchema:
        """router facing method to update a cpu metric

        Args:
            cpu_metric_table (Table): cpu metric table
            cpu_metric (CpuMetricUpdateSchema): cpu metric data

        Returns:
            CpuMetricSchema: updated cpu metric data
        """
        item_data = cpu_metric.model_dump(exclude_none=True)

        update_expressions = []
        expression_values = {}

        for key, value in item_data.items():
            if key != "id":  # Don't update the primary key
                update_expressions.append(f"{key} = :{key}")
                expression_values[f":{key}"] = value

        if not update_expressions:
            raise InvalidRequestException("No update fields provided")

        update_expression = "SET " + ", ".join(update_expressions)

        try:
            response = cpu_metric_table.update_item(
                Key={"id": item_data["id"]},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW",
            )
        except ClientError as err:
            print(f"ClientError: {err}")
            raise ServerException()
        else:
            return CpuMetricSchema(**response.get("Attributes", {}))

    def delete_cpu_metric(self, cpu_metric_table: Table, cpu_metric_id: str) -> CpuMetricSchema:
        """router facing method to delete a cpu metric

        Args:
            cpu_metric_table (Table): cpu metric table
            cpu_metric_id (str): cpu metric id

        Returns:
            CpuMetricSchema: deleted cpu metric data
        """
        try:
            response = cpu_metric_table.delete_item(Key={"id": cpu_metric_id}, ReturnValues="ALL_OLD")
        except ClientError as err:
            print(f"ClientError: {err}")
            raise ServerException()
        else:
            return CpuMetricSchema(**response.get("Attributes", {}))
