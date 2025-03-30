"""
Config Manager

The config manager is used to manage the configuration settings for the application. The settings are loaded from the .env file
and can be accessed using the config_manager object.

Author: Tom Aston
"""

import os
from enum import Enum
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load the .env file from aws/ecs/
dotenv_path = os.path.abspath("aws/ecs/.env")
load_dotenv(dotenv_path, override=True)


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

    # General app config----------------------------------
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "CPU Metrics API"
    PROJECT_DESCRIPTION: str = "A simple API to retrieve Raspberry Pi CPU metrics from DynamoDB"

    # AWS DynamoDB config-------------------------------
    DB_TABLE_NAME: str
    DYNAMODB_ENDPOINT: str = "http://localhost:9000"
    DYNAMODB_REGION: str

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

    # AWS Cognito config-------------------------------
    COGNITO_USER_POOL_ID: str
    COGNITO_USER_POOL_CLIENT_ID: str
    COGNITO_USER_POOL_REGION: str
    COGNITO_JWT_SECRET: str
    COGNITO_CLIENT_SECRET: str

    # Test config---------------------------------------
    TEST_USERNAME: str
    TEST_PASSWORD: str
    TEST_EMAIL: str

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = ""
        extra = "allow"


config_manager = ConfigManager()
