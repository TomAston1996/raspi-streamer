"""
Schema for the CPU metrics
Author: Tom Aston
"""

from typing import Optional

from pydantic import BaseModel


class CpuMetricSchema(BaseModel):
    unit: str
    loop_count: int
    project: str
    topic: str
    location: str
    cpu_usage: int
    device: str
    version: str
    timestamp: int


class CpuMetricFilterRequestSchema(BaseModel):
    key: str
    value: int | str
    operator: str  # eq, gt, lt
