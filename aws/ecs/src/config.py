"""
Config Manager
Author: Tom Aston
"""

from pydantic_settings import BaseSettings


class ConfigManager(BaseSettings):
    """
    ConfigManager
    """

    # app config-----------------------------------------
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "CPU Metrics API"
    PROJECT_DESCRIPTION: str = "A simple API to retrieve Raspberry Pi CPU metrics from DynamoDB"
    # ---------------------------------------------------

    # AWS DynamoDB config-------------------------------
    DB_TABLE_NAME: str
    # ---------------------------------------------------

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = ""


config_manager = ConfigManager()
