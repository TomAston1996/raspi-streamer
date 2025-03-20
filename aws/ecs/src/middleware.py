"""
Module to register middleware
Author: Tom Aston
"""

import logging
import time
from typing import Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.requests import Request
from fastapi.responses import Response

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI) -> None:
    """
    Register middleware
    """

    # Add custom logging middleware
    @app.middleware("http")
    def custom_logging(request: Request, call_next: Callable[[Request], Response]) -> Response:
        """custom logging middleware

        Args:
            request (Request): request to intercept
            call_next (Callable[[Request], Response]): next middleware or route handler

        Returns:
            Response: returns the response after middleware processing
        """        
        start_time = time.time()  # start time

        response: Response = call_next(request)  # call the next middleware or route handler

        process_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} {request.method} {request.url.path} {response.status_code} - Completed in {process_time}s"

        print(message)

        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add TrustedHostMiddleware
    # This middleware checks the Host header of the request against a list of allowed hosts.
    # * At the moment trusted hosts are set to just localhost
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "test"])