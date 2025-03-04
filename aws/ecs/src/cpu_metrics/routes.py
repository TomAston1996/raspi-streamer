"""
CPU Metrics routes
Author: Tom Aston
"""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, status
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import CpuMetricQueryParams, CpuMetricSchema
from .service import CpuMetricsService

cpu_metrics_router = APIRouter()
cpu_metrics_service = CpuMetricsService()
from ..database import get_db_table


@cpu_metrics_router.get("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def get_all_cpu_metrics(
    params: CpuMetricQueryParams = Depends(),
    db_table: Table = Depends(get_db_table),
) -> List[CpuMetricSchema]:
    """get endpoint for all cpu metrics
    will return all cpu metrics if no query parameters are provided

    Args:
        params (CpuMetricQueryParams, optional): query parameters. Defaults to Depends().
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        List[CpuMetricSchema]: list of cpu metrics data with all attributes included
    """    
    print(f'params: {params}')
    return cpu_metrics_service.get_cpu_metrics(cpu_metric_table=db_table, params=params)
