"""
Module to define the payload structure for the CPU metric
Author: Tom Aston
"""

from typing import TypedDict


class CPUMetricPayload(TypedDict):
    """
    CPU Metric Payload dictionary
    """

    cpu_usage: int
    timestamp: float
    device: str
    location: str
    unit: str
    topic: str
    loop_count: int
    project: str
    version: str
