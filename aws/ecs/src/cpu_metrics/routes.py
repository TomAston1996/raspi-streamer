"""
CPU Metrics routes
Author: Tom Aston
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, status
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import CpuMetricFilterRequestSchema, CpuMetricSchema
from .service import CpuMetricsService

cpu_metrics_router = APIRouter()
cpu_metrics_service = CpuMetricsService()
from ..database import get_db_table


@cpu_metrics_router.get("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def get_all_cpu_metrics(
    key: Optional[str] = None,
    value: Optional[str | int] = None,
    operator: Optional[str] = None,
    db_table: Table = Depends(get_db_table),
) -> List[CpuMetricSchema]:
    """
    Get CPU Metrics
    """
    print(f"key: {key}, value: {value}, operator: {operator}")
    return cpu_metrics_service.get_cpu_metrics(cpu_metric_table=db_table, key=key, value=value, operator=operator)
