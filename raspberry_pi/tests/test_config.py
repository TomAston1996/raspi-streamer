"""
Test suite for the config manager.
Author: Tom Aston
"""

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pydantic import ValidationError

from ..src.config import ConfigManager


class TestSuiteConfigManager:
    """
    Test suite for the config manager.
    """

    @pytest.fixture
    def config_manager(self, monkeypatch: MonkeyPatch) -> ConfigManager:
        monkeypatch.setenv("RPI_AWS_IOT_ENDPOINT", "test-endpoint")
        monkeypatch.setenv("RPI_AWS_IOT_CERTIFICATE", "test-certificate")
        monkeypatch.setenv("RPI_AWS_IOT_PRIVATE_KEY", "test-private-key")
        monkeypatch.setenv("RPI_AWS_IOT_ROOT_CA", "test-root-ca")
        config_manager = ConfigManager()
        return config_manager

    def test_env_loading(self, config_manager: ConfigManager) -> None:
        """
        Test if the config manager loads environment variables correctly.
        """
        assert config_manager.RPI_AWS_IOT_ENDPOINT == "test-endpoint"
        assert config_manager.RPI_AWS_IOT_CERTIFICATE == "test-certificate"
        assert config_manager.RPI_AWS_IOT_PRIVATE_KEY == "test-private-key"
        assert config_manager.RPI_AWS_IOT_ROOT_CA == "test-root-ca"

    def test_default_values(self, config_manager: ConfigManager) -> None:
        """
        Test if the config manager loads default values correctly.
        """
        assert config_manager.VERSION == "0.0.1"
        assert config_manager.PROJECT_NAME == "Raspberry Pi IoT"
        assert config_manager.PROJECT_DESCRIPTION == "A simple IoT project for Raspberry Pi"

    def test_missing_required_env(self, monkeypatch: MonkeyPatch) -> None:
        """
        Test if the config manager raises an exception when a required environment variable is missing.
        """
        monkeypatch.delenv("RPI_AWS_IOT_ENDPOINT", raising=False)
        monkeypatch.delenv("RPI_AWS_IOT_CERTIFICATE", raising=False)

        # Override the env_file setting
        class TestConfigManager(ConfigManager):
            class Config:
                env_file = None  # Disable .env loading

        with pytest.raises(ValidationError):
            TestConfigManager()
