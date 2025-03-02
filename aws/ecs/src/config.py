"""
Config Manager
Author: Tom Aston
"""

from enum import Enum

from pydantic_settings import BaseSettings


class EnvrinomentEnum(Enum):
    """
    EnvrinomentEnum
    """

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class ConfigManager(BaseSettings):
    """
    ConfigManager
    """

    ENVIRONMENT: EnvrinomentEnum = EnvrinomentEnum.LOCAL

    # app config-----------------------------------------
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "CPU Metrics API"
    PROJECT_DESCRIPTION: str = "A simple API to retrieve Raspberry Pi CPU metrics from DynamoDB"
    # ---------------------------------------------------

    # AWS DynamoDB config-------------------------------
    DB_TABLE_NAME: str
    DYNAMODB_ENDPOINT: str = "http://localhost:9000"
    DYNAMODB_REGION: str
    # ---------------------------------------------------

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = ""


config_manager = ConfigManager()
