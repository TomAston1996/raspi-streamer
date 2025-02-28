"""
CPU Metrics routes
Author: Tom Aston
"""

from typing import List

from fastapi import APIRouter, Depends, status

from .service import CpuMetricsService

cpu_metrics_router = APIRouter()
cpu_metrics_service = CpuMetricsService()


@cpu_metrics_router.get("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def get_all_cpu_metrics() -> List[dict[str, str]]:
    """
    Get CPU Metrics
    """
    return cpu_metrics_service.get_all_cpu_metrics()
