"""
Schema for the CPU metrics
Author: Tom Aston
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class CpuMetricSchema(BaseModel):
    id: str
    unit: str
    loop_count: int
    project: str
    topic: str
    location: str
    cpu_usage: int
    device: str
    version: str
    timestamp: int


class CpuMetricQueryParams(BaseModel):
    location_value: Optional[Literal["Home", "Office", "Factory", "*"]] = Field(
        None, description="Allowed locations are Home, Office, Factory, or *"
    )
    operator: Optional[Literal["eq", "gt", "lt", "*"]] = Field(
        None, description="Allowed operators are eq, gt, lt or *"
    )
    cpu_usage_value: Optional[int] = Field(None, ge=0, le=100, description="CPU usage value (0-100)")


class CpuMetricCreateSchema(BaseModel):
    unit: str
    loop_count: int
    project: str
    topic: str
    location: str
    cpu_usage: int
    device: str
    version: str
