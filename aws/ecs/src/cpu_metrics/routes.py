"""
CPU Metrics API routes

Routes for the CPU Metrics API including get, post, put, and delete endpoints. The routes are used to interact with the 
CPU Metrics data in the DynamoDB table.

Author: Tom Aston
"""

from typing import Any, List

from fastapi import APIRouter, Depends, status
from mypy_boto3_dynamodb.service_resource import Table

from .schemas import CpuMetricCreateSchema, CpuMetricQueryParams, CpuMetricSchema, CpuMetricUpdateSchema
from .service import CpuMetricsService

cpu_metrics_router = APIRouter()
cpu_metrics_service = CpuMetricsService()
from src.auth.service import oauth2_scheme

from ..databases.dynamo_db import get_db_table


@cpu_metrics_router.get("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def get_all_cpu_metrics(
    params: CpuMetricQueryParams = Depends(),
    db_table: Table = Depends(get_db_table),
    _=Depends(oauth2_scheme),
) -> List[CpuMetricSchema]:
    """get endpoint for all cpu metrics
    will return all cpu metrics if no query parameters are provided

    Args:
        params (CpuMetricQueryParams, optional): query parameters. Defaults to Depends().
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        List[CpuMetricSchema]: list of cpu metrics data with all attributes included
    """
    print(f"params: {params}")
    return cpu_metrics_service.get_cpu_metrics(cpu_metric_table=db_table, params=params)


@cpu_metrics_router.post("", tags=["cpu_metrics"], status_code=status.HTTP_201_CREATED)
def create_cpu_metric(
    cpu_metric: CpuMetricCreateSchema,
    db_table: Table = Depends(get_db_table),
    _=Depends(oauth2_scheme),
) -> CpuMetricSchema:
    """post endpoint to create a cpu metric

    Args:
        cpu_metric (CpuMetricCreateSchema): cpu metric data
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        CpuMetricSchema: created cpu metric data
    """
    return cpu_metrics_service.create_cpu_metric(cpu_metric_table=db_table, cpu_metric=cpu_metric)


@cpu_metrics_router.post("/batch", tags=["cpu_metrics"], status_code=status.HTTP_201_CREATED)
def batch_create_cpu_metrics(
    cpu_metrics: List[CpuMetricCreateSchema],
    db_table: Table = Depends(get_db_table),
    _=Depends(oauth2_scheme),
) -> List[CpuMetricSchema]:
    """post endpoint to create multiple cpu metrics

    Args:
        cpu_metrics (List[CpuMetricCreateSchema]): list of cpu metric data
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        List[CpuMetricSchema]: list of created cpu metric data
    """
    print(f"cpu_metrics: {cpu_metrics}")
    return cpu_metrics_service.batch_create_cpu_metrics(cpu_metric_table=db_table, cpu_metrics=cpu_metrics)


@cpu_metrics_router.put("", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def update_cpu_metric(
    cpu_metric: CpuMetricUpdateSchema,
    db_table: Table = Depends(get_db_table),
    _=Depends(oauth2_scheme),
) -> CpuMetricSchema:
    """put endpoint to update a cpu metric

    Args:
        cpu_metric (CpuMetricSchema): cpu metric data
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        CpuMetricSchema: updated cpu metric data
    """
    return cpu_metrics_service.update_cpu_metric(cpu_metric_table=db_table, cpu_metric=cpu_metric)


@cpu_metrics_router.delete("/{cpu_metric_id}", tags=["cpu_metrics"], status_code=status.HTTP_200_OK)
def delete_cpu_metric(
    cpu_metric_id: str,
    db_table: Table = Depends(get_db_table),
    _=Depends(oauth2_scheme),
) -> Any:
    """delete endpoint to delete a cpu metric

    Args:
        cpu_metric_id (str): cpu metric id
        db_table (Table, optional): db table. Defaults to Depends(get_db_table).

    Returns:
        Any: response
    """
    return cpu_metrics_service.delete_cpu_metric(cpu_metric_table=db_table, cpu_metric_id=cpu_metric_id)
