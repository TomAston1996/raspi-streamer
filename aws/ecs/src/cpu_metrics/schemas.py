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


class CpuMetricUpdateSchema(BaseModel):
    id: str
    unit: Optional[str] = Field(None, description="Unit of measurement")
    loop_count: Optional[int] = Field(None, description="Loop count")
    project: Optional[str] = Field(None, description="Project name")
    topic: Optional[str] = Field(None, description="Topic")
    location: Optional[str] = Field(None, description="Location")
    cpu_usage: Optional[int] = Field(None, description="CPU usage value")
    device: Optional[str] = Field(None, description="Device")
    version: Optional[str] = Field(None, description="Version")
