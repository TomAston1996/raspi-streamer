"""
Global fixtures for tests
Author: Tom Aston
"""

import time
import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from src.cpu_metrics.schemas import CpuMetricCreateSchema, CpuMetricSchema
from src.main import app


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """test client fixture

    Returns:
        TestClient: test client
    """
    yield TestClient(app)


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


@pytest.fixture
def test_cpu_metrics_response_json() -> CpuMetricSchema:
    """test repspone to get all cpu metrics

    Returns:
        List[CpuMetricSchema]: dummy json payload
    """
    return [
        CpuMetricSchema(
            location="Home",
            cpu_usage=10,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
            id=str(uuid.uuid4()),
            timestamp=int(time.time()),
        ),
        CpuMetricSchema(
            location="Office",
            cpu_usage=20,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
            id=str(uuid.uuid4()),
            timestamp=int(time.time()),
        ),
        CpuMetricSchema(
            location="Factory",
            cpu_usage=30,
            unit="percent",
            loop_count=1,
            project="test",
            topic="test",
            device="test",
            version="1.0",
            id=str(uuid.uuid4()),
            timestamp=int(time.time()),
        ),
    ]


def mock_client() -> TestClient:
    """
    Test client
    """
    return TestClient(app)
