"""
module for dynamodb table operations
Author: Tom Aston
"""

import os
import uuid
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from mypy_boto3_dynamodb import DynamoDBServiceResource

try:
    dynamo_db_client: DynamoDBServiceResource = boto3.resource("dynamodb")
    CPU_METRIC_TABLE_NAME = os.environ["DB_TABLE_NAME"]
    cpu_metric_table = dynamo_db_client.Table(CPU_METRIC_TABLE_NAME)
except KeyError:
    raise RuntimeError("DB_TABLE_NAME environment variable not set")


def put_item(event: dict[str, Any]) -> None:
    """put an item into the DynamoDB table

    Args:
        event (dict[str, Any]): event data
    """    
    try:
        item = {
            "device": event["device"],
            "timestamp": int(event["timestamp"]),
            "cpu_usage": float(event["cpu_usage"]),
            "id": str(uuid.uuid4()),
        }

        cpu_metric_table.put_item(Item=item)
        print("Item successfully put into DynamoDB:", item)

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
