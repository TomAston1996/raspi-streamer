"""
Authentication service module.

The authentication service module provides the functionality to sign up, sign in, confirm email, reset password,
and log out a user from the Cognito user pool. The purpose of the module is to provide the business logic for the
authentication routes.

Author: Tom Aston
"""

import boto3
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from src.config import config_manager
from src.errors import ServerException

from .model import Token, User
from .utils import decode_jwt, get_secret_hash

COGNITO_CLIENT_ID = config_manager.COGNITO_USER_POOL_CLIENT_ID
COGNITO_REGION = config_manager.COGNITO_USER_POOL_REGION
JWT_SECRET = config_manager.COGNITO_JWT_SECRET
COGNITO_CLIENT_SECRET = config_manager.COGNITO_CLIENT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    """Authentication service class
    
    The authentication service class provides the functionality to sign up, sign in, confirm email, reset password,
    and log out a user from the Cognito user pool.
    """

    def __init__(self) -> None:
        """initialize the authentication service class
        """        
        self.cognito_client: CognitoIdentityProviderClient = boto3.client("cognito-idp", region_name=COGNITO_REGION)

    def signup(self, user: User) -> User:
        """sign up a user to the Cognito user pool

        Args:
            user (User): user details including username, password and email

        Raises:
            HTTPException: if the username already exists
            ServerException: internal server error

        Returns:
            User: user details
        """
        try:
            secret_hash = get_secret_hash(user.username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

            self.cognito_client.sign_up(
                ClientId=COGNITO_CLIENT_ID,
                SecretHash=secret_hash,
                Username=user.username,
                Password=user.password,
                UserAttributes=[
                    {"Name": "email", "Value": user.email},
                ],
            )
            return user
        except self.cognito_client.exceptions.UsernameExistsException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        except Exception as e:
            print(e)
            raise ServerException("An error occurred while signing up the user")

    def verify_email(self, user: User) -> dict[str, str]:
        """confirm the user's email via cognito confirmation code

        Args:
            user (User): user details with added confirmation code

        Raises:
            ServerException: internal server error

        Returns:
            dict[str, str]: confirmation message
        """
        try:
            secret_hash = get_secret_hash(user.username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

            response = self.cognito_client.confirm_sign_up(
                ClientId=COGNITO_CLIENT_ID,
                SecretHash=secret_hash,
                Username=user.username,
                ConfirmationCode=user.confirmation_code,
            )

            return {"message": "Email confirmed"}
        except Exception as e:
            print(f"Exception: {e}")
            raise ServerException("An error occurred while confirming the user's email")

    def signin(self, user: User) -> Token:
        """sign in a user to the Cognito user pool

        Args:
            user (User): user details

        Raises:
            HTTPException: if the username or password is incorrect
            ServerException: internal server error

        Returns:
            Token: JWT token
        """
        try:
            secret_hash = get_secret_hash(user.username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

            response = self.cognito_client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": user.username,
                    "PASSWORD": user.password,
                    "SECRET_HASH": secret_hash,
                },
            )

            access_token = response["AuthenticationResult"]["AccessToken"]

            # token = create_jwt_token(user.username)
            return Token(access_token=access_token, token_type="bearer")
        except self.cognito_client.exceptions.NotAuthorizedException as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or password is incorrect",
            )
        except Exception as e:
            print(e)
            raise ServerException("An error occurred while signing in the user")

    def logout(self, token: str) -> dict[str, str]:
        """log out a user from the Cognito user pool

        Args:
            token (str, optional): JWT token. Defaults to Depends(oauth2_scheme).

        Raises:
            ServerException: internal server error

        Returns:
            dict: logout message
        """
        try:
            # will raise an error if the token is invalid
            decode_jwt(token)

            self.cognito_client.global_sign_out(
                AccessToken=token,
            )
            return {"message": f"Successfully logged out"}
        except Exception as e:
            print(e)
            raise ServerException("An error occurred while logging out the user")

    def reset_password(self, user: User) -> dict[str, str]:
        """reset the user's password

        Args:
            user (User): user details

        Raises:
            ServerException: internal server error

        Returns:
            dict: reset password message
        """
        try:
            secret_hash = get_secret_hash(user.username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

            self.cognito_client.confirm_forgot_password(
                ClientId=COGNITO_CLIENT_ID,
                SecretHash=secret_hash,
                Username=user.username,
                ConfirmationCode=user.confirmation_code,
                Password=user.password,
            )
            return {"message": "Password has been reset"}
        except Exception as e:
            print(e)
            raise ServerException("An error occurred while resetting the user's password")

    def get_current_user(self, token: str) -> str:
        """get the current user

        Args:
            token (str, optional): JWT token. Defaults to Depends(oauth2_scheme).

        Raises:
            HTTPException: if the token is invalid

        Returns:
            str: username
        """
        decoded_token = decode_jwt(token)
        return decoded_token["username"]
