"""
Schema for the CPU metrics
Author: Tom Aston
"""

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
