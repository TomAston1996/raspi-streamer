"""
CPU Metrics routes
Author: Tom Aston
"""

from typing import Any, List

from fastapi import APIRouter, Depends, status
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import CpuMetricSchema
from .service import CpuMetricsService

cpu_metrics_router = APIRouter()
cpu_metrics_service = CpuMetricsService()
from ..database import get_db_table


@cpu_metrics_router.get("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def get_all_cpu_metrics(db_table: Table = Depends(get_db_table)) -> List[CpuMetricSchema]:
    """
    Get CPU Metrics
    """
    return cpu_metrics_service.get_all_cpu_metrics(db_table)
