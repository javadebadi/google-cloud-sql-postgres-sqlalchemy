"""Google Cloud SQL PostgreSQL SQLAlchemy connector.

This package provides utilities for creating SQLAlchemy engines that work with
PostgreSQL databases, both locally and on Google Cloud SQL.
"""

from .cloud_sql_proxy import cloud_sql_proxy_running, get_cloud_sql_proxy_path
from .create_engine import (
    create_database_engine,
    create_postgres_engine,
    create_postgres_engine_in_cloud_sql,
)

__version__ = "0.2.0"

__all__ = [
    "cloud_sql_proxy_running",
    "create_database_engine",
    "create_postgres_engine",
    "create_postgres_engine_in_cloud_sql",
    "get_cloud_sql_proxy_path",
]
