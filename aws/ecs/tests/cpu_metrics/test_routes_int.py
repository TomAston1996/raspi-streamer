"""
Integrations tests for the routes module
Author: Tom Aston
"""
# *NOTE: requires docker to be running for integration tests to pass

from random import choice

import pytest
from fastapi.testclient import TestClient
from src.config import config_manager
from src.cpu_metrics.schemas import CpuMetricCreateSchema


class TestIntegrationCpuMetricRoutes:
    """
    Test suite for the routes module in CPU Metrics API
    """

    BASE_URL = f"/api/{config_manager.VERSION}/cpu_metrics"

    def test_get_all_cpu_metrics(self, test_client: TestClient) -> None:
        """test get all cpu metrics

        Args:
            test_client (TestClient): test client from conftest.py
        """
        response = test_client.get(self.BASE_URL)
        assert response.status_code == 200
        assert len(response.json()) > 0

    @pytest.mark.parametrize("location_value", ["Home", "Office", "Factory"])
    def test_get_cpu_metric_by_location(self, location_value: str, test_client: TestClient) -> None:
        """test get cpu metric by location

        Args:
            test_client (TestClient): test client from conftest.py
        """
        # query will get all cpu metrics as we are scanning for all cases where cpu usage is greater than 0 (which will be all results)
        OPERATOR = "gt"
        CPU_USAGE_VALUE = 0

        response = test_client.get(
            f"{self.BASE_URL}?location_value={location_value}&operator={OPERATOR}&cpu_usage_value={CPU_USAGE_VALUE}"
        )

        assert response.status_code == 200
        for cpu_metric in response.json():
            assert location_value == cpu_metric["location"]

    @pytest.mark.parametrize("operator", ["gt", "lt"])
    def test_get_cpu_metric_by_cpu_usage(self, operator: str, test_client: TestClient) -> None:
        """test get cpu metric by cpu usage

        Args:
            test_client (TestClient): test client from conftest.py
        """
        CPU_USAGE_VALUE = 50
        response = test_client.get(
            f"{self.BASE_URL}?location_value=*&operator={operator}&cpu_usage_value={CPU_USAGE_VALUE}"
        )

        assert response.status_code == 200
        for cpu_metric in response.json():
            if operator == "gt":
                assert cpu_metric["cpu_usage"] > CPU_USAGE_VALUE
            elif operator == "lt":
                assert cpu_metric["cpu_usage"] < CPU_USAGE_VALUE

    def test_create_cpu_metric(self, test_client: TestClient, test_create_payload: list[CpuMetricCreateSchema]) -> None:
        """test create cpu metric

        Args:
            test_client (TestClient): test client from conftest.py
            test_create_payload (list[CpuMetricCreateSchema]): cpu metric payload
        """
        payload = test_create_payload[0].model_dump()

        response = test_client.post(self.BASE_URL, json=payload)

        assert response.status_code == 201
        assert response.json()["location"] == payload["location"]
        assert response.json()["cpu_usage"] == payload["cpu_usage"]

    def test_batch_create_cpu_metrics(
        self, test_client: TestClient, test_create_payload: list[CpuMetricCreateSchema]
    ) -> None:
        """test batch create cpu metrics

        Args:
            test_client (TestClient): test client from conftest.py
            test_create_payload (list[CpuMetricCreateSchema]): cpu metric payload
        """
        payload = [cpu_metric.model_dump() for cpu_metric in test_create_payload]

        response = test_client.post(f"{self.BASE_URL}/batch", json=payload)

        assert response.status_code == 201
        assert len(response.json()) == len(payload)

    def test_update_cpu_metric(self, test_client: TestClient, test_create_payload: list[CpuMetricCreateSchema]) -> None:
        """test update cpu metric

        Args:
            test_client (TestClient): test client from conftest.py
            test_create_payload (list[CpuMetricCreateSchema]): cpu metric payload
        """

        def get_random_int_exclude(number_to_exclude: int) -> int:
            return choice([i for i in range(0, 100) if i != number_to_exclude])

        payload = test_create_payload[0].model_dump()
        create_response = test_client.post(self.BASE_URL, json=payload)
        cpu_metric_id = create_response.json()["id"]

        new_cpu_usage = get_random_int_exclude(payload["cpu_usage"])
        update_payload = {"id": cpu_metric_id, "cpu_usage": new_cpu_usage}

        update_response = test_client.put(self.BASE_URL, json=update_payload)

        assert update_response.status_code == 200
        assert update_response.json()["cpu_usage"] == new_cpu_usage
        assert update_response.json()["id"] == cpu_metric_id

    def test_delete_cpu_metric(self, test_client: TestClient, test_create_payload: list[CpuMetricCreateSchema]) -> None:
        """test delete cpu metric

        Args:
            test_client (TestClient): test client from conftest.py
            test_create_payload (list[CpuMetricCreateSchema]): test payload
        """
        payload = test_create_payload[0].model_dump()
        create_response = test_client.post(self.BASE_URL, json=payload)
        cpu_metric_id = create_response.json()["id"]

        delete_response = test_client.delete(f"{self.BASE_URL}/{cpu_metric_id}")

        assert delete_response.status_code == 200
        assert delete_response.json()["id"] == cpu_metric_id

    def test_create_cpu_metric_missing_fields(self, test_client: TestClient) -> None:
        """test create cpu metric with missing fields

        Args:
            test_client (TestClient): test client from conftest.py
        """
        response = test_client.post(self.BASE_URL, json={})

        assert response.status_code == 422

    def test_update_cpu_metric_missing_fields(self, test_client: TestClient) -> None:
        """test update cpu metric with missing fields

        Args:
            test_client (TestClient): test client from conftest.py
        """        

        invalid_payload = {"location": 123, "cpu_usage": "invalid_string"}
        
        response = test_client.put(self.BASE_URL, json=invalid_payload)

        assert response.status_code == 422
