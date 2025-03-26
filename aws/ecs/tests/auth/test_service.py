"""
Unit tests for the service module in authentication API

Author: Tom Aston
"""

from unittest.mock import Mock, patch

import pytest
from src.auth.model import User
from src.auth.service import AuthService


class TestUnitAuthService:
    """
    Unit tests for the authentication service module in the Auth API
    """

    @pytest.fixture
    def sample_user(self) -> User:
        """mock user fixture

        Returns:
            User: mock user object
        """
        return User(username="test_user", password="test_password", email="test_email")

    @pytest.fixture
    def auth_service(self) -> AuthService:
        """auth service fixture

        Returns:
            AuthService: auth service object
        """
        return AuthService()

    def test_signup(self, sample_user: User, auth_service: AuthService) -> None:
        """test signup method

        Args:
            sample_user (User): mock user object
            auth_service (AuthService): auth service object
        """
        auth_service.cognito_client.sign_up = Mock()
        auth_service.signup(sample_user)
        auth_service.cognito_client.sign_up.assert_called_once()

    def test_verify_email(self, sample_user: User, auth_service: AuthService) -> None:
        """test verify email method

        Args:
            sample_user (User): mock user object
            auth_service (AuthService): auth service object
        """
        auth_service.cognito_client.confirm_sign_up = Mock()
        actual_response = auth_service.verify_email(sample_user)
        auth_service.cognito_client.confirm_sign_up.assert_called_once()
        assert actual_response == {"message": "Email confirmed"}
