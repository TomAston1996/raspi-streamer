'''
Module to interact with DynamoDB database

The CpuMetricDatabase class is used to interact with the DynamoDB table that stores the CPU metrics data.
There are functions to create the table, check if it exists, and populate it with test data.

Author: Tom Aston
'''

import random
import time
import uuid
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb import DynamoDBClient, DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table

from ..config import EnvrinomentEnum, config_manager

if config_manager.ENVIRONMENT == EnvrinomentEnum.LOCAL:
    dynamodb_client = boto3.client(
        "dynamodb", region_name=config_manager.DYNAMODB_REGION, endpoint_url=config_manager.DYNAMODB_ENDPOINT
    )
    dynamodb_resource = boto3.resource(
        "dynamodb", region_name=config_manager.DYNAMODB_REGION, endpoint_url=config_manager.DYNAMODB_ENDPOINT
    )
else:  # Production (ECS)
    dynamodb_client = boto3.client("dynamodb")
    dynamodb_resource = boto3.resource("dynamodb")


class CpuMetricDatabase:
    """
    DynamoDB Database
    """

    def __init__(
        self, table_name: str, dynamodb_resource: DynamoDBServiceResource, dynamodb_client: DynamoDBClient
    ) -> None:
        self.table_name = table_name
        self.resource = dynamodb_resource
        self.client = dynamodb_client

    def get_table(self) -> Table:
        """
        Get the DynamoDB table
        """
        try:
            table = self.resource.Table(self.table_name)
            return table
        except ClientError as err:
            raise RuntimeError(f"Error getting table: {err}") from err

    def table_exists(self) -> bool:
        """Check if the DynamoDB table exists"""
        try:
            self.client.describe_table(TableName=self.table_name)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return False
            raise e

    def create_table(self) -> None:
        """
        Create the DynamoDB table
        """
        try:
            table = self.resource.create_table(
                TableName=config_manager.DB_TABLE_NAME,
                AttributeDefinitions=[
                    {"AttributeName": "id", "AttributeType": "S"},  # Partition Key
                    {"AttributeName": "timestamp", "AttributeType": "N"},  # GSI Sort Key
                    {"AttributeName": "cpu_usage", "AttributeType": "N"},  # GSI Partition Key
                    {"AttributeName": "location", "AttributeType": "S"},  # GSI Partition Key
                ],
                KeySchema=[
                    {"AttributeName": "id", "KeyType": "HASH"},  # Primary Key
                ],
                BillingMode="PAY_PER_REQUEST",  # On-demand billing
                GlobalSecondaryIndexes=[
                    {
                        "IndexName": "TimestampCpuUsageIndex",
                        "KeySchema": [
                            {"AttributeName": "cpu_usage", "KeyType": "HASH"},  # GSI Partition Key
                            {"AttributeName": "timestamp", "KeyType": "RANGE"},  # GSI Sort Key
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                    },
                    {
                        "IndexName": "LocationIndex",
                        "KeySchema": [
                            {"AttributeName": "location", "KeyType": "HASH"},  # GSI Partition Key
                            {"AttributeName": "cpu_usage", "KeyType": "RANGE"},  # GSI Sort Key
                        ],
                        "Projection": {"ProjectionType": "ALL"},
                    },
                ],
            )
            print("Creating table, please wait...")
            table.wait_until_exists()
            print("Table created successfully!")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":
                print("Table already exists.")
            else:
                raise e  # Re-raise unexpected errors

    def populate_test_data(self, num_test_records: int = 5) -> None:
        """Populate the CPUMetrics table with test data."""
        table: Table = self.get_table()

        for _ in range(num_test_records):
            test_data = {
                "id": str(uuid.uuid4()),
                "cpu_usage": random.randint(1, 100),  # Random CPU usage %
                "timestamp": int(time.time()),  # Current timestamp
                "device": f"raspberry_pi_{random.randint(1, 10)}",
                "location": random.choice(["Home", "Office", "Factory"]),
                "unit": "%",
                "topic": "cpu_metrics/device",
                "loop_count": random.randint(1, 10),
                "project": "Raspberry Pi CPU Metrics API",
                "version": "1.0",
            }

            table.put_item(Item=test_data)


@lru_cache()
def get_database() -> CpuMetricDatabase:
    """Create and cache a Database instance."""
    return CpuMetricDatabase(config_manager.DB_TABLE_NAME, dynamodb_resource, dynamodb_client)


def get_db_table() -> Table:
    """Retrieve the DynamoDB table."""
    return get_database().get_table()


# Initialize the database only in LOCAL environment
if config_manager.ENVIRONMENT == EnvrinomentEnum.LOCAL:
    db = get_database()
    if not db.table_exists():
        db.create_table()
        db.populate_test_data()
    else:
        print("Table already exists, skipping creation and test data population.")
