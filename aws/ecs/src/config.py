"""
Config Manager
Author: Tom Aston
"""

from enum import Enum
from functools import cached_property

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

    # Postgres User config-------------------------------
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST_PORT: str
    POSTGRES_HOST_NAME: str
    USER_DB_ENGINE: str = "postgresql"

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    @cached_property
    def USER_DATABASE_URI(self) -> str:
        return self.DATABASE_URI_FORMAT.format(
            db_engine=self.USER_DB_ENGINE,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST_NAME,
            port=self.POSTGRES_HOST_PORT,
            database=self.POSTGRES_DB,
        )
    # ---------------------------------------------------

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = ""


config_manager = ConfigManager()
