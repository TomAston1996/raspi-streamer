"""
Unit tests for the service module.
Author: Tom Aston
"""

from unittest.mock import MagicMock, Mock

import pytest
from src.cpu_metrics.schemas import CpuMetricCreateSchema, CpuMetricQueryParams
from src.cpu_metrics.service import CpuMetricsService


class TestUnitCpuMetricsService:
    """
    Unit tests for the service module in CPU Metrics API
    """

    @pytest.fixture
    def mock_db_table(self) -> Mock:
        """mock db table fixture

        Returns:
            Mock: mock of db table
        """
        return Mock()

    @pytest.mark.parametrize(
        "query_params",
        [
            CpuMetricQueryParams(),
            CpuMetricQueryParams(location_value="Home", operator="gt", cpu_usage_value=0),
            CpuMetricQueryParams(location_value="*", operator="gt", cpu_usage_value=0),
        ],
    )
    def test_get_all_cpu_metrics(self, query_params: CpuMetricQueryParams, mock_db_table: Mock) -> None:
        """test filter cpu metrics logic

        Args:
            mock_db_table (Mock): db table mock
        """
        cpu_metrics_service = CpuMetricsService()

        # mock the protected methods
        cpu_metrics_service._get_all_cpu_metrics = Mock()
        cpu_metrics_service._get_filtered_cpu_metrics = Mock()
        cpu_metrics_service._get_all_devices_filtered_by_cpu_usage = Mock()

        # call the get cpu metrics method
        cpu_metrics_service.get_cpu_metrics(cpu_metric_table=mock_db_table, params=query_params)

        if query_params.location_value and query_params.operator and query_params.cpu_usage_value is not None:
            cpu_metrics_service._get_filtered_cpu_metrics.assert_called_once_with(mock_db_table, params=query_params)
        else:
            cpu_metrics_service._get_all_cpu_metrics.assert_called_once_with(mock_db_table)

    def test_get_all_cpu_metrics_with_location_wildcard(self, mock_db_table: Mock) -> None:
        """test get all cpu metrics with location wildcard

        Args:
            mock_db_table (Mock): db table mock
        """
        cpu_metrics_service = CpuMetricsService()

        # mock the protected methods
        cpu_metrics_service._get_all_devices_filtered_by_cpu_usage = Mock()

        query_params = CpuMetricQueryParams(location_value="*", operator="gt", cpu_usage_value=0)

        # call the get cpu metrics method
        cpu_metrics_service.get_cpu_metrics(cpu_metric_table=mock_db_table, params=query_params)

        cpu_metrics_service._get_all_devices_filtered_by_cpu_usage.assert_called_once_with(
            mock_db_table, query_params.cpu_usage_value, query_params.operator
        )

    def test_create_cpu_metric(self, mock_db_table: Mock, test_create_payload: list[CpuMetricCreateSchema]) -> None:
        """test create cpu metric. make sure the put_item method is called and the response has an id and timestamp

        Args:
            mock_db_table (Mock): mock of db table
            test_create_payload (list[CpuMetricCreateSchema]): payload to create cpu metric from conftest.py
        """
        mock_db_table.put_item = Mock()

        single_create_payload = test_create_payload[0]

        cpu_metrics_service = CpuMetricsService()

        single_create_payload = test_create_payload[0]
        response = cpu_metrics_service.create_cpu_metric(
            cpu_metric_table=mock_db_table, cpu_metric=single_create_payload
        )

        mock_db_table.put_item.assert_called_once()
        assert response["timestamp"] is not None
        assert response["id"] is not None

    def test_batch_create_cpu_metrics(self, test_create_payload: list[CpuMetricCreateSchema]) -> None:
        """test batch create cpu metrics

        Args:
            mock_db_table (Mock): mock of db table
            test_create_payload (list[CpuMetricCreateSchema]): payload to create cpu metric from conftest.py
        """
        mock_db_table = MagicMock()
        cpu_metrics_service = CpuMetricsService()

        response = cpu_metrics_service.batch_create_cpu_metrics(
            cpu_metric_table=mock_db_table, cpu_metrics=test_create_payload
        )

        assert len(response) == len(test_create_payload)
        for item in response:
            assert item["timestamp"] is not None
            assert item["id"] is not None
