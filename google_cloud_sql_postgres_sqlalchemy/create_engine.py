"""SQLAlchemy engine creation utilities for PostgreSQL and Google Cloud SQL."""

import sqlalchemy
from google.cloud.sql.connector import Connector
from pg8000.dbapi import Connection as PG8000Connection
from sqlalchemy import URL, Engine, create_engine

from .cloud_sql_proxy import is_valid_cloud_sql_instance_name


def create_postgres_engine(
    username: str,
    password: str,
    host: str,
    database: str,
) -> Engine:
    """Create a Postgres SQLAlchemy engine instance.

    This is used to create a connection pool for the Postgres database when
    postgres is not hosted on Google Cloud SQL.

    Args:
        username: Database username
        password: Database password
        host: Database host
        database: Database name

    Returns:
        SQLAlchemy Engine instance
    """
    url_object = URL.create(
        "postgresql+pg8000",
        username=username,
        password=password,
        host=host,
        database=database,
    )
    return create_engine(url_object)


def create_postgres_engine_in_cloud_sql(
    username: str,
    password: str,
    host: str,
    database: str,
) -> Engine:
    """Create a Postgres SQLAlchemy engine instance for Cloud SQL.

    This is used to create a connection pool for the Postgres database when
    postgres is hosted on Google Cloud SQL.

    Args:
        username: Database username
        password: Database password
        host: Cloud SQL instance connection name (format: project:region:instance)
        database: Database name

    Returns:
        SQLAlchemy Engine instance configured for Cloud SQL

    Raises:
        ValueError: If the instance connection name format is invalid
    """
    # Validate instance connection name format
    if not is_valid_cloud_sql_instance_name(host):
        raise ValueError(
            f"Invalid Cloud SQL instance connection name: '{host}'. "
            "Expected format: 'project-id:region:instance-name' "
            "(e.g., 'my-project:us-central1:my-instance')",
        )

    # Initialize Cloud SQL connector
    connector = Connector()

    def get_cloud_sql_connector() -> PG8000Connection:
        """Return a Cloud SQL Connector object.

        This is used to create secure connections to the Cloud SQL instance.
        """
        conn = connector.connect(
            host,  # instance connection name
            "pg8000",
            user=username,
            password=password,
            db=database,
        )
        if conn is None:
            raise RuntimeError("Failed to create Cloud SQL connection")
        return conn

    # use SQLAlchemy for ORM-style connection pooling
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=get_cloud_sql_connector,
    )
    return engine


def create_database_engine(
    username: str,
    password: str,
    host: str,
    database: str,
    google_cloud_project_id: str | None = None,
) -> Engine:
    """Create a SQLAlchemy engine for Postgres.

    This function creates either a Cloud SQL engine or a regular Postgres engine
    based on whether a Google Cloud project ID is provided.

    Args:
        username: Database username
        password: Database password
        host: Database host (instance connection name for Cloud SQL)
        database: Database name
        google_cloud_project_id: Optional Google Cloud project ID. If provided,
            creates a Cloud SQL connector-based engine. Otherwise creates a
            standard Postgres engine.

    Returns:
        SQLAlchemy Engine instance
    """
    # Build the appropriate engine based on whether we are using Cloud SQL or not
    if google_cloud_project_id:
        return create_postgres_engine_in_cloud_sql(
            username=username,
            password=password,
            host=host,
            database=database,
        )
    else:
        return create_postgres_engine(
            username=username,
            password=password,
            host=host,
            database=database,
        )
