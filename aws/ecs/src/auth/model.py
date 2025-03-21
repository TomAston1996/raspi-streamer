"""
This file contains the routes for the authentication module.
The routes are used to authenticate the user and provide a token for accessing the API.

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
