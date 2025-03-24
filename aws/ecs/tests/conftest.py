"""
Global fixtures for tests
Author: Tom Aston
"""

import time
import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from src.config import config_manager
from src.cpu_metrics.schemas import CpuMetricCreateSchema, CpuMetricSchema
from src.main import app


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    """test client fixture

    This fixture will create a test client for the FastAPI app. The fixture will run once per session
    as its scope is session.

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


@pytest.fixture(scope="session")  # only need to get the auth token once
def auth_token(test_client: TestClient) -> str:
    """get auth token

    This fixture will get the auth token for the test user. The fixure will run once per session
    as its scope is session.

    Args:
        test_client (TestClient): test client from conftest.py
    """

    base_auth_url = f"/api/{config_manager.VERSION}/auth"

    response = test_client.post(
        f"{base_auth_url}/signin",
        json={
            "username": config_manager.TEST_USERNAME,
            "password": config_manager.TEST_PASSWORD,
            "email": config_manager.TEST_EMAIL,
        },
    )

    return response.json()["access_token"]
