"""
Unit tests for the auth utils module
Author: Tom Aston
"""

import base64
import hashlib
import hmac
from unittest.mock import MagicMock, patch

import jwt
import pytest
from src.auth.utils import (
    AccessTokenException,
    InvalidTokenException,
    ServerException,
    decode_jwt,
    get_cognito_public_keys,
    get_secret_hash,
)


class TestUnitAuthUtils:
    """
    Test suite for the auth utils module in the Auth API
    """

    @pytest.fixture
    def sample_token(self) -> str:
        """return a sample jwt token

        Returns:
            str: mock jwt token
        """
        return "valid.jwt.token"

    @pytest.fixture
    def sample_public_keys(self) -> list[dict[str, str]]:
        """return a sample list of public keys

        Returns:
            list[dict[str, str]]: mock list of public keys
        """
        return [{"kid": "test_kid", "alg": "RS256"}]

    @pytest.fixture
    def sample_decoded_token(self) -> dict[str, str]:
        """fixture for returning a decoded token

        Returns:
            dict[str, str]: mock decoded token
        """
        return {"token_use": "access", "sub": "123456789"}

    @patch("src.auth.utils.get_cognito_public_keys")
    @patch("jwt.get_unverified_header")
    @patch("jwt.algorithms.RSAAlgorithm.from_jwk")
    @patch("jwt.decode")
    def test_decode_jwt_valid(
        self,
        mock_decode: MagicMock,
        mock_from_jwk: MagicMock,
        mock_get_unverified_header: MagicMock,
        mock_get_cognito_public_keys: MagicMock,
        sample_token: str,
        sample_public_keys: list[dict[str, str]],
        sample_decoded_token: dict[str, str],
    ) -> None:
        """test decoding a valid jwt token

        Args:
            mock_decode (MagicMock): mock object for jwt.decode
            mock_from_jwk (MagicMock): mock object for jwt.algorithms.RSAAlgorithm.from_jwk
            mock_get_unverified_header (MagicMock): mock object for jwt.get_unverified_header
            mock_get_cognito_public_keys (MagicMock): mock object for get_cognito_public_keys
            sample_token (str): mock jwt token
            sample_public_keys (list[dict[str, str]]): mock list of public keys
            sample_decoded_token (dict[str, str]): mock decoded token
        """
        mock_get_cognito_public_keys.return_value = sample_public_keys
        mock_get_unverified_header.return_value = {"kid": "test_kid"}
        mock_decode.return_value = sample_decoded_token

        # Simulate an actual public key (mocked object)
        mock_public_key = MagicMock()
        mock_from_jwk.return_value = mock_public_key

        result = decode_jwt(sample_token)
        assert result == sample_decoded_token

    @patch("src.auth.utils.get_cognito_public_keys")
    @patch("jwt.get_unverified_header")
    def test_decode_jwt_missing_key(
        self, mock_get_unverified_header: MagicMock, mock_get_cognito_public_keys: MagicMock
    ) -> None:
        """test decoding a jwt token with a missing key

        Args:
            mock_get_unverified_header (MagicMock): mock object for jwt.get_unverified_header
            mock_get_cognito_public_keys (MagicMock): mock object for get_cognito_public_keys
        """
        mock_get_cognito_public_keys.return_value = []
        mock_get_unverified_header.return_value = {"kid": "unknown_kid"}

        with pytest.raises(ValueError):
            decode_jwt("valid.jwt.token")

    @patch("src.auth.utils.get_cognito_public_keys")
    @patch("jwt.get_unverified_header")
    @patch("jwt.algorithms.RSAAlgorithm.from_jwk")
    @patch("jwt.decode")
    def test_decode_jwt_wrong_token_use(
        self,
        mock_decode: MagicMock,
        mock_from_jwk: MagicMock,
        mock_get_unverified_header: MagicMock,
        mock_get_cognito_public_keys: MagicMock,
        sample_token: str,
        sample_public_keys: list[dict[str, str]],
    ) -> None:
        """test decoding a jwt token with the wrong token use

        In this case, the token use is not "access" but "id" therefore an AccessTokenException
        should be raised

        Args:
            mock_decode (MagicMock): mock object for jwt.decode
            mock_get_unverified_header (MagicMock): mock object for jwt.get_unverified_header
            mock_get_cognito_public_keys (MagicMock): mock object for get_cognito_public_keys
            sample_token (str): mock jwt token
            sample_public_keys (list[dict[str, str]]): mock list of public keys
        """

        mock_get_cognito_public_keys.return_value = sample_public_keys
        mock_get_unverified_header.return_value = {"kid": "test_kid"}
        mock_decode.return_value = {"token_use": "id", "sub": "123456789"}  # Should be "access"

        # Simulate an actual public key (mocked object)
        mock_public_key = MagicMock()
        mock_from_jwk.return_value = mock_public_key

        with pytest.raises(AccessTokenException):
            decode_jwt(sample_token)

    @patch("src.auth.utils.get_cognito_public_keys")
    @patch("jwt.get_unverified_header")
    @patch("jwt.algorithms.RSAAlgorithm.from_jwk")
    @patch("jwt.decode", side_effect=jwt.ExpiredSignatureError)
    def test_decode_jwt_expired_token(
        self,
        mock_decode: MagicMock,
        mock_from_jwk: MagicMock,
        mock_get_unverified_header: MagicMock,
        mock_get_cognito_public_keys: MagicMock,
        sample_token: str,
        sample_public_keys: list[dict[str, str]],
    ) -> None:
        """test decoding a jwt token with expired signature

        In this case, the jwt.decode method raises an ExpiredSignatureError which should be caught
        and an InvalidTokenException should be raised

        Args:
            mock_decode (MagicMock): mock object for jwt.decode
            mock_get_unverified_header (MagicMock): mock object for jwt.get_unverified_header
            mock_get_cognito_public_keys (MagicMock): mock object for get_cognito_public_keys
            sample_token (str): mock jwt token
            sample_public_keys (list[dict[str, str]]): mock list of public keys
        """
        mock_get_cognito_public_keys.return_value = sample_public_keys
        mock_get_unverified_header.return_value = {"kid": "test_kid"}

        # Simulate an actual public key (mocked object)
        mock_public_key = MagicMock()
        mock_from_jwk.return_value = mock_public_key

        with pytest.raises(InvalidTokenException):
            decode_jwt(sample_token)

    @patch("src.auth.utils.get_cognito_public_keys")
    @patch("jwt.get_unverified_header")
    @patch("jwt.algorithms.RSAAlgorithm.from_jwk")
    @patch("jwt.decode", side_effect=Exception("Unexpected Error"))
    def test_decode_jwt_server_exception(
        self,
        mock_decode: MagicMock,
        mock_from_jwk: MagicMock,
        mock_get_unverified_header: MagicMock,
        mock_get_cognito_public_keys: MagicMock,
        sample_token: str,
        sample_public_keys: list[dict[str, str]],
    ) -> None:
        """test decoding a jwt token with a server exception

        In this case, the jwt.decode method raises an unexpected error which should be caught
        and a ServerException should be raised

        Args:
            mock_decode (MagicMock): mock object for jwt.decode
            mock_get_unverified_header (MagicMock): mock object for jwt.get_unverified_header
            mock_get_cognito_public_keys (MagicMock): mock object for get_cognito_public_keys
            sample_token (str): mock jwt token
            sample_public_keys (list[dict[str, str]]): mock list of public keys
        """
        mock_get_cognito_public_keys.return_value = sample_public_keys
        mock_get_unverified_header.return_value = {"kid": "test_kid"}

        # Simulate an actual public key (mocked object)
        mock_public_key = MagicMock()
        mock_from_jwk.return_value = mock_public_key

        with pytest.raises(ServerException):
            decode_jwt(sample_token)

    @pytest.mark.parametrize(
        "username,client_id,client_secret",
        [
            ("testuser", "clientid123", "clientsecret456"),
            ("anotheruser", "clientidXYZ", "clientsecretABC"),
        ],
    )
    def test_get_secret_hash(self, username: str, client_id: str, client_secret: str) -> None:
        """test getting a secret hash for a user

        This test is based on the following logic:
        1. Concatenate the username and client_id
        2. Use the client_secret to hash the concatenated string
        3. Encode the hashed value in base64 and return it as the secret hash for the user

        Args:
            username (str): _description_
            client_id (str): _description_
            client_secret (str): _description_
        """
        expected_message = username + client_id
        expected_digest = hmac.new(client_secret.encode(), expected_message.encode(), hashlib.sha256).digest()
        expected_hash = base64.b64encode(expected_digest).decode()

        result = get_secret_hash(username, client_id, client_secret)
        assert result == expected_hash
