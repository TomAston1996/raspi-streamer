"""
Return schemas for Lambda function responses
Author: Tom Aston
"""

import json
from typing import Any, TypedDict


class LambdaInvokeResponse(TypedDict):
    """
    Response schema
    """

    message: str
    status_code: int
    headers: dict


def create_response(status_code: int, message: dict[str, Any]) -> LambdaInvokeResponse:
    """create a response dictionary
    Args:
        status_code (int): http status code
        message (dict[str, Any]): message to return

    Returns:
        dict: dictionary containing the response
    """
    return LambdaInvokeResponse(
        message=json.dumps(message),
        status_code=status_code,
        headers={
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Method": "*",
        },
    )
