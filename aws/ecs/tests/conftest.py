"""
Global fixtures for tests
Author: Tom Aston
"""

import pytest
from fastapi.testclient import TestClient
from src.cpu_metrics.schemas import CpuMetricCreateSchema
from src.main import app


@pytest.fixture
def test_client() -> TestClient:
    """test client fixture

    Returns:
        TestClient: test client
    """
    return TestClient(app)


@pytest.fixture
def test_create_payload() -> list[CpuMetricCreateSchema]:
    """test payload

    Returns:
        list[dict[str, str]]: dummy json payload
    """
    return [
        CpuMetricCreateSchema(
            location="Home",
            cpu_usage=10,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
        ),
        CpuMetricCreateSchema(
            location="Office",
            cpu_usage=20,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
        ),
        CpuMetricCreateSchema(
            location="Factory",
            cpu_usage=30,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
        ),
    ]
