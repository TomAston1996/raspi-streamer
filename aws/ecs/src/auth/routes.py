"""
This file contains the routes for the authentication module.
The routes are used to authenticate the user and provide a token for accessing the API.

Author: Tom Aston
"""

from fastapi import APIRouter, Depends

from .model import Token, User
from .service import AuthService, oauth2_scheme

auth_router = APIRouter()

auth_service = AuthService()


@auth_router.post("/signup", response_model=User)
def signup(user: User) -> User:
    """route to sign up a user

    Args:
        user (User): user details including username, password and email

    Returns:
        User: user details
    """
    return auth_service.signup(user)


@auth_router.post("/confirm", response_model=dict[str, str])
def confirm(user: User) -> dict[str, str]:
    """route to confirm the user's email

    Args:
        user (User): user details including confirmation code

    Returns:
        dict[str, str]: confirmation message
    """
    return auth_service.verify_email(user)


@auth_router.post("/signin", response_model=Token)
def signin(user: User) -> Token:
    """route to sign in a user

    Args:
        user (User): user details including username and password

    Returns:
        Token: jwt access token
    """
    return auth_service.signin(user)


@auth_router.post("/logout", response_model=dict[str, str])
def logout(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    """route to log out a user from the Cognito user pool

    Args:
        token (str, optional): JWT token. Defaults to Depends(oauth2_scheme).

    Returns:
        dict: logout message
    """
    return auth_service.logout(token)


@auth_router.post("/reset_password", response_model=dict[str, str])
def reset_password(user: User) -> dict[str, str]:
    """route to reset the user's password

    Args:
        user (User): user details including username, password and confirmation code

    Returns:
        dict: reset password message
    """
    return auth_service.reset_password(user)


@auth_router.get("/current_user", response_model=str)
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """route to get the current user

    Args:
        token (str, optional): JWT token. Defaults to Depends(oauth2_scheme).

    Returns:
        str: username
    """
    return auth_service.get_current_user(token)
