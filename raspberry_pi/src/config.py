"""
Config Manager
Author: Tom Aston
"""

from pydantic_settings import BaseSettings


class ConfigManager(BaseSettings):
    """
    Config manager
    """

    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "Raspberry Pi IoT"
    PROJECT_DESCRIPTION: str = "A simple IoT project for Raspberry Pi"

    # AWS IoT Core
    RPI_AWS_IOT_ENDPOINT: str
    RPI_AWS_IOT_CERTIFICATE: str
    RPI_AWS_IOT_PRIVATE_KEY: str
    RPI_AWS_IOT_ROOT_CA: str

    class Config:
        """
        config will read from .env file in the root directory
        """

        env_file = ".env"
        env_prefix = ""


config_manager = ConfigManager()

if __name__ == "__main__":
    print(config_manager.RPI_AWS_IOT_ENDPOINT)
    print(config_manager.RPI_AWS_IOT_CERTIFICATE)
    print(config_manager.RPI_AWS_IOT_PRIVATE_KEY)
    print(config_manager.RPI_AWS_IOT_ROOT_CA)
    print(config_manager.VERSION)
    print(config_manager.PROJECT_NAME)
    print(config_manager.PROJECT_DESCRIPTION)
