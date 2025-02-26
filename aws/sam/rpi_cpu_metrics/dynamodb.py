"""
module for dynamodb table operations
Author: Tom Aston
"""

import json
import os
import uuid
from decimal import Decimal
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from mypy_boto3_dynamodb import DynamoDBServiceResource
from rpi_cpu_metrics.schemas import CpuMetricMessageBody, SQSEvent

try:
    dynamo_db_client: DynamoDBServiceResource = boto3.resource("dynamodb")
    CPU_METRIC_TABLE_NAME = os.environ["DB_TABLE_NAME"]
    cpu_metric_table = dynamo_db_client.Table(CPU_METRIC_TABLE_NAME)
except KeyError:
    raise RuntimeError("DB_TABLE_NAME environment variable not set")


def put_item(event: SQSEvent) -> CpuMetricMessageBody:
    """put an item into the DynamoDB table

    Args:
        event (SQSEvent): event data
    """
    try:
        database_item = __create_database_item(event)

        if not database_item:
            raise ValueError("Issue parsing SQS event records")

        item = json.loads(
            json.dumps(database_item), parse_float=Decimal
        )  # convert float to Decimal to avoid serialization issues

        cpu_metric_table.put_item(Item=item)
        print("Item successfully put into DynamoDB:", item)
        return database_item
    except ValueError as e:
        print(f"ValueError: {e}")
        raise
    except ClientError as e:
        print(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        raise RuntimeError("DynamoDB operation failed") from e
    except BotoCoreError as e:
        print(f"BotoCoreError: {str(e)}")
        raise RuntimeError(f"AWS SDK error occurred: {str(e)}") from e
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise RuntimeError("Error putting item into DynamoDB")


def __create_database_item(event: SQSEvent) -> dict[str, Any] | None:
    """parse through the event data and create a dictionary to be inserted into the database

    Args:
        event (SQSEvent): sqs event data

    Returns:
        dict[str, Any]: database item
    """
    for record in event["Records"]:
        sns_message: dict = json.loads(record["body"])
        if sns_message.get("Message"):
            message_body: CpuMetricMessageBody = json.loads(sns_message["Message"])
            cpu_usage = message_body.get("cpu_usage")
            timestamp = message_body.get("timestamp")
            device = message_body.get("device")
            location = message_body.get("location")
            unit = message_body.get("unit")
            topic = message_body.get("topic")
            loop_count = message_body.get("loop_count")
            project = message_body.get("project")
            version = message_body.get("version")
            id = str(uuid.uuid4())

            item = {
                "device": device,
                "timestamp": int(timestamp),
                "cpu_usage": float(cpu_usage),
                "id": id,
                "location": location,
                "unit": unit,
                "topic": topic,
                "loop_count": int(loop_count),
                "project": project,
                "version": version,
            }

            print("Database item created within function:", item)
            return item
