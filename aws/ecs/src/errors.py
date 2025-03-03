"""
This module contains all the custom exceptions that are raised in the fastapi app
Author: Tom Aston
"""

from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Base class for all custom exceptions
    """

    pass


class InvalidRequestException(AppException):
    """
    Exception raised for invalid requests
    """

    pass


class ServerException(AppException):
    """
    Exception raised for server errors
    """

    pass


def create_exception_hander(status_code: int, detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    """
    Factory function that creates an exception handler for a given status code and detail
    """

    async def exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """
        Exception handler for a given status code and detail
        """
        return JSONResponse(
            status_code=status_code,
            content={"message": str(detail)},
        )

    return exception_handler


def register_all_errors(app: FastAPI) -> None:
    """
    Registers all the custom exceptions in the Bookly App
    """
    app.add_exception_handler(
        InvalidRequestException,
        create_exception_hander(status.HTTP_400_BAD_REQUEST, "Invalid request parameters or body"),
    )

    app.add_exception_handler(
        ServerException,
        create_exception_hander(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"),
    )
