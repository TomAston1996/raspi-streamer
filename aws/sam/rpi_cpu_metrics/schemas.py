"""
This module contains the dataclasses that represent the structure of the SQS event that is sent to the Lambda function.
Author: Tom Aston
"""

from typing import Dict, List, TypedDict


class SQSEventRecord(TypedDict):
    """SQS event record schema

    Keys:
        messageId: str
        receiptHandle: str
        body: str  # JSON-encoded string, needs parsing
        attributes: Dict[str, str]
        messageAttributes: Dict[str, Dict]
        md5OfBody: str
        eventSource: str
        eventSourceARN: str
        awsRegion: str
    """

    messageId: str
    receiptHandle: str
    body: str  # JSON-encoded string, needs parsing
    attributes: Dict[str, str]
    messageAttributes: Dict[str, Dict]
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class SQSEvent(TypedDict):
    """SQS event schema

    Keys:
        Records: List[SQSEventRecord]
    """

    Records: List[SQSEventRecord]


class CpuMetricMessageBody(TypedDict):
    """cpu metric message body

    Keys:
        cpu_usage: int
        timestamp: float
        device: str
        location: str
        unit: str
        topic: str
        loop_count: int
        project: str
        version: str
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
