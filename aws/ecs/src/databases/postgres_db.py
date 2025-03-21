"""
Postgres Database for Users

This module contains the database class for the Users database. It is used to create the database tables and get the database session.
This could potentially be used for user custom authorisation in the future - whereas AWS Cognito would be used for user authentication. 
At the moment however, the database is not used.

Author: Tom Aston
"""

from typing import Any, Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeMeta, Session, declarative_base, sessionmaker
from src.config import config_manager

BaseModel: DeclarativeMeta = declarative_base()
metadata = MetaData()


class UsersDatabase:
    """
    User database class
    """

    def __init__(self, db_url: str) -> None:
        """user database constructor

        Args:
            db_url (str): database url
        """
        self.engine = create_engine(
            db_url,
            echo=False,  # Set to True to see SQL queries in the console on FastAPI
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=Session)

    def create_database(self) -> None:
        """Create all the database tables defined in models if they don't already exist"""
        BaseModel.metadata.create_all(self.engine)

    def get_db(self) -> Generator[Session, None, None]:
        """get the database session

        Yields:
            Generator[Session, None, None]: database session
        """
        db: Session = self.session_local()
        try:
            yield db
        finally:
            db.close()


# Instantiate the database object
users_database = UsersDatabase(config_manager.USER_DATABASE_URI)
