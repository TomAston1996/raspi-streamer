"""
Helper functions for authentication including decoding JWT tokens and creating JWT tokens.

The get public keys function gets the public keys from AWS Cognito and the decode JWT function
decodes the JWT token. The get secret hash function gets the secret hash for the user and the create
JWT token function creates a JWT token for the user.

Author: Tom Aston
"""

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta

import jwt
import jwt.algorithms
import requests
from fastapi import HTTPException
from src.config import config_manager
from src.errors import AccessTokenException, InvalidTokenException, ServerException

USER_POOL_ID = config_manager.COGNITO_USER_POOL_ID
CLIENT_ID = config_manager.COGNITO_USER_POOL_CLIENT_ID
COGNITO_REGION = config_manager.COGNITO_USER_POOL_REGION
COGNITO_KEYS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"


def get_cognito_public_keys() -> dict:
    """
    Get the public keys from AWS Cognito

    Returns:
        dict: public keys
    """
    return requests.get(COGNITO_KEYS_URL).json()["keys"]


def decode_jwt(token: str) -> dict:
    """decode the JWT token from AWS Cognito

    Args:
        token (str): jwt token

    Raises:
        ValueError: raised when the public key is not found in the JWKs
        AccessTokenException: raised when the token use is not access token
        InvalidTokenException: raised when the token is invalid due to expired signature or invalid token
        ServerException: raised when there is an internal server error

    Returns:
        dict: decoded token
    """
    keys = get_cognito_public_keys()
    header = jwt.get_unverified_header(token)

    # Find the matching key
    key = next((key for key in keys if key["kid"] == header["kid"]), None)
    if key is None:
        raise ValueError("Public key not found in JWKs")

    # Convert the JWK to PEM format
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))

    try:
        # Decode and verify the token
        decoded_token: dict = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}",
        )

        if decoded_token.get("token_use") != "access":
            raise AccessTokenException()

        return decoded_token
    except jwt.ExpiredSignatureError as ese:
        raise InvalidTokenException()
    except jwt.InvalidTokenError as ite:
        raise InvalidTokenException()
    except AccessTokenException as ate:
        raise ate
    except Exception as e:
        raise ServerException()


def get_secret_hash(username: str, client_id: str, client_secret: str) -> str:
    """get the secret hash for the user

    Args:
        username (str): username of the user
        client_id (str): client id provided by AWS Cognito client app
        client_secret (str): client secret key provided by AWS Cognito client app
    Returns:
        str: secret hash for the user
    """
    message = username + client_id
    dig = hmac.new(client_secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(dig).decode()


def create_jwt_token(username: str) -> str:
    """
    #! DEPRECATED FUNCTION ----> USE AWS Cognito to create JWT token
    Create a JWT token for the user

    Args:
        username (str): username

    Returns:
        str: JWT token
    """
    payload = {"sub": username, "exp": datetime.now() + timedelta(hours=1)}

    return jwt.encode(payload, config_manager.COGNITO_JWT_SECRET, algorithm="HS256")


def decode_jwt_token(token: str) -> dict:
    """
    #! DEPRECATED ----> USE decode_jwt(token: str) instead
    Decode the JWT token

    Args:
        token (str): JWT token

    Returns:
        dict: decoded token
    """
    try:
        return jwt.decode(token, config_manager.COGNITO_JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Oops! Something went wrong")
