'''
CPU metric handler lambda function
Author: Tom Aston
'''

import json

from aws_lambda_powertools.utilities.typing import LambdaContext


def handler(event: dict, context: LambdaContext) -> dict[str, str]:
    '''
    handler function for the CPU metric lambda function
    '''
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "function triggered",
            "timestamp": event["timestamp"],
            "device": event["device"],
        }),
    }
