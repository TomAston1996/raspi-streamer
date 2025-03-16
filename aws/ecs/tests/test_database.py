"""
Test cases for the database module.
Author: Tom Aston
"""

from unittest.mock import Mock

import pytest

from src.databases.dynamo_db import CpuMetricDatabase
from mypy_boto3_dynamodb import DynamoDBClient, DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table


class TestUnitDatabase:
    """
    Unit tests for the database module in CPU Metrics API
    """

    @pytest.fixture
    def mock_database_object(self) -> CpuMetricDatabase:
        """mock database object fixture

        Returns:
            Mock: mock of database object
        """
        table_name: str = "TestTable"

        dynamodb_resource = Mock(spec=DynamoDBServiceResource)
        dynamodb_client = Mock(spec=DynamoDBClient)
        mock_db = Database(table_name, dynamodb_resource, dynamodb_client)
        
        return mock_db

    def test_get_table(self, mock_database_object: CpuMetricDatabase) -> None:
        """test get table method

        Args:
            mock_database_object (Database): mock database object
        """
        mock_database_object.resource.Table = Mock()
        mock_database_object.get_table()
        mock_database_object.resource.Table.assert_called_once_with(mock_database_object.table_name)

    def test_table_exists(self, mock_database_object: CpuMetricDatabase) -> None:
        """test table exists method

        Args:
            mock_database_object (Database): mock database object
        """
        mock_database_object.client.describe_table = Mock()
        mock_database_object.table_exists()
        mock_database_object.client.describe_table.assert_called_once_with(TableName=mock_database_object.table_name)

    def test_create_table(self, mock_database_object: CpuMetricDatabase) -> None:
        """test create table method

        Args:
            mock_database_object (Database): mock database object
        """
        mock_database_object.resource.create_table = Mock()
        mock_database_object.create_table()
        mock_database_object.resource.create_table.assert_called_once()

    def test_table_exists_exception(self, mock_database_object: CpuMetricDatabase) -> None:
        """test table exists method with exception

        Args:
            mock_database_object (Database): mock database object
        """
        mock_database_object.client.describe_table = Mock(side_effect=Exception)
        with pytest.raises(Exception):
            mock_database_object.table_exists()

    @pytest.mark.parametrize("number_of_items", [5, 10, 20])
    def test_populate_test_data(self, number_of_items: int, mock_database_object: CpuMetricDatabase) -> None:
        """test populate test data method

        Args:
            number_of_items (int): number of items to populate the table with
            mock_database_object (Database): mock database object
        """
        mock_database_object.resource.Table.put_item = Mock()
        mock_database_object.populate_test_data(num_test_records=number_of_items)
        assert mock_database_object.resource.Table().put_item.call_count == number_of_items
