"""
This file contains the models for the authentication module.

The models are used to define the structure of the data that is passed between the client and the server.

Author: Tom Aston
"""

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str
    confirmation_code: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
