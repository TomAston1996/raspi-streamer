"""
Service module for CPU metrics
Author: Tom Aston
"""

from typing import Any


class CpuMetricsService:
    """
    CPU Metrics Service
    """
    
    def get_all_cpu_metrics(self) -> list[Any]:
        """
        Get all CPU metrics
        """
        return [{"message": "CPU Metrics"}]
