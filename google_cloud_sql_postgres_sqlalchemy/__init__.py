"""Google Cloud SQL PostgreSQL SQLAlchemy connector.

This package provides utilities for creating SQLAlchemy engines that work with
PostgreSQL databases, both locally and on Google Cloud SQL.
"""

from .create_engine import (
    create_database_engine,
    create_postgres_engine,
    create_postgres_engine_in_cloud_sql,
)

__version__ = "0.1.0"

__all__ = [
    "create_database_engine",
    "create_postgres_engine",
    "create_postgres_engine_in_cloud_sql",
]
