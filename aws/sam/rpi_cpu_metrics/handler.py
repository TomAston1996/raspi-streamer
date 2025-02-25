"""
CPU metric handler lambda function
Author: Tom Aston
"""

import os
from http import HTTPStatus
from typing import Any

import rpi_cpu_metrics.dynamodb as CPU_METRICS_DB
from aws_lambda_powertools.utilities.typing import LambdaContext
from common.schemas import LambdaInvokeResponse, create_response


def handler(event: dict[str, Any], context: LambdaContext) -> LambdaInvokeResponse:
    """lambda function handler for putting cpu metrics into a DynamoDB table

    Args:
        event (dict): dictionary containing the event data
        context (LambdaContext): lambda context object

    Returns:
        dict[str, str]: dictionary containing the response message
    """
    if not _check_all_attributes_present(event):
        return create_response(
            status_code=HTTPStatus.BAD_REQUEST,
            message={"error": "missing required attributes"},
        )

    try:
        CPU_METRICS_DB.put_item(event=event)

        return create_response(
            status_code=HTTPStatus.OK,
            message={
                "message": "function triggered",
                "timestamp": event["timestamp"],
                "device": event["device"],
            },
        )
    except Exception as e:
        return create_response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message={"error": str(e)},
        )


def _check_all_attributes_present(event: dict[str, Any]) -> bool:
    """check all required attributes are present in the event

    Args:
        event (dict): dictionary containing the event data

    Returns:
        bool: True if all attributes are present, False otherwise
    """
    return all([event.get("device"), event.get("cpu_usage"), event.get("timestamp")])
