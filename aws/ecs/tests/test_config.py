"""
Config Unit Test
Author: Tom Aston
"""

import pytest
from src.config import ConfigManager


class TestConfig:
    """
    Test Config Manager
    """

    @pytest.fixture
    def config_manager(self) -> ConfigManager:
        """
        Config Manager
        """
        return ConfigManager()

    def test_config_db_parameters(self, config_manager: ConfigManager):
        """
        Test config manager params are present
        """
        assert config_manager.DB_TABLE_NAME is not None
        assert config_manager.PROJECT_NAME is not None
        assert config_manager.VERSION is not None
        assert config_manager.PROJECT_DESCRIPTION is not None
