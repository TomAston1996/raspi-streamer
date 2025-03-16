"""
FastAPI app entry point
Author: Tom Aston
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.routes import auth_router
from .config import config_manager
from .cpu_metrics.routes import cpu_metrics_router
from .errors import register_all_errors


class AppCreator:
    """
    Application Context Creator
    """

    def __init__(self) -> None:
        """
        initialise the app creator
        """

        self.app = FastAPI(
            title=config_manager.PROJECT_NAME,
            description=config_manager.PROJECT_DESCRIPTION,
            version=config_manager.VERSION,
        )

        @self.app.get("/", tags=["root"])
        def root() -> dict[str, str]:
            """root endpoint

            Returns:
                dict[str, str]: server is running message
            """
            return {"message": "server is running"}

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.include_router(cpu_metrics_router, prefix=f"/api/{config_manager.VERSION}/cpu_metrics")
        self.app.include_router(auth_router, prefix=f"/api/{config_manager.VERSION}/auth")

        register_all_errors(self.app)


app_creator = AppCreator()
app = app_creator.app
