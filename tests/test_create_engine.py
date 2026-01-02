"""Tests for the create_engine module."""

from unittest.mock import Mock, patch

import pytest
from sqlalchemy import Engine

from google_cloud_sql_postgres_sqlalchemy import (
    create_database_engine,
    create_postgres_engine,
    create_postgres_engine_in_cloud_sql,
)


def test_create_postgres_engine() -> None:
    """Test creating a regular Postgres engine."""
    # Given database connection parameters
    username = "test_user"
    password = "test_password"
    host = "localhost"
    database = "test_db"

    # When I create a Postgres engine
    engine = create_postgres_engine(
        username=username,
        password=password,
        host=host,
        database=database,
    )

    # Then I should get a SQLAlchemy Engine instance
    assert isinstance(engine, Engine)
    assert "postgresql+pg8000" in str(engine.url)
    assert username in str(engine.url)
    assert host in str(engine.url)
    assert database in str(engine.url)


@patch("google_cloud_sql_postgres_sqlalchemy.create_engine.Connector")
def test_create_postgres_engine_in_cloud_sql(mock_connector_class: Mock) -> None:
    """Test creating a Cloud SQL Postgres engine."""
    # Given database connection parameters
    username = "test_user"
    password = "test_password"
    host = "test-project:us-central1:test-instance"
    database = "test_db"

    # And a mock Cloud SQL connector
    mock_connector = Mock()
    mock_connection = Mock()
    mock_connector.connect.return_value = mock_connection
    mock_connector_class.return_value = mock_connector

    # When I create a Cloud SQL Postgres engine
    engine = create_postgres_engine_in_cloud_sql(
        username=username,
        password=password,
        host=host,
        database=database,
    )

    # Then I should get a SQLAlchemy Engine instance
    assert isinstance(engine, Engine)
    assert "postgresql+pg8000" in str(engine.url)

    # And the connector should be initialized
    mock_connector_class.assert_called_once()


def test_create_database_engine_without_cloud_sql() -> None:
    """Test creating engine without Cloud SQL."""
    # Given database connection parameters without Google Cloud project ID
    username = "test_user"
    password = "test_password"
    host = "localhost"
    database = "test_db"

    # When I create an engine without google_cloud_project_id
    engine = create_database_engine(
        username=username,
        password=password,
        host=host,
        database=database,
        google_cloud_project_id=None,
    )

    # Then it should create a regular Postgres engine
    assert isinstance(engine, Engine)
    assert "postgresql+pg8000" in str(engine.url)
    assert username in str(engine.url)
    assert host in str(engine.url)


@patch("google_cloud_sql_postgres_sqlalchemy.create_engine.Connector")
def test_create_database_engine_with_cloud_sql(mock_connector_class: Mock) -> None:
    """Test creating engine with Cloud SQL."""
    # Given database connection parameters with Google Cloud project ID
    username = "test_user"
    password = "test_password"
    host = "test-project:us-central1:test-instance"
    database = "test_db"

    # And a mock Cloud SQL connector
    mock_connector = Mock()
    mock_connection = Mock()
    mock_connector.connect.return_value = mock_connection
    mock_connector_class.return_value = mock_connector

    # When I create an engine with google_cloud_project_id
    engine = create_database_engine(
        username=username,
        password=password,
        host=host,
        database=database,
        google_cloud_project_id="test-project",
    )

    # Then it should create a Cloud SQL engine
    assert isinstance(engine, Engine)
    assert "postgresql+pg8000" in str(engine.url)


@patch("google_cloud_sql_postgres_sqlalchemy.create_engine.Connector")
def test_create_postgres_engine_in_cloud_sql_successful_connection(
    mock_connector_class: Mock,
) -> None:
    """Test successful Cloud SQL connection creation through creator function."""
    # Given database connection parameters
    username = "test_user"
    password = "test_password"
    host = "test-project:us-central1:test-instance"
    database = "test_db"

    # And a mock connector that returns a valid connection
    mock_connector = Mock()
    mock_connection = Mock()
    mock_connection.py_types = {str: str}  # Mock the pg8000 attribute
    mock_connector.connect.return_value = mock_connection
    mock_connector_class.return_value = mock_connector

    # When I create a Cloud SQL Postgres engine
    engine = create_postgres_engine_in_cloud_sql(
        username=username,
        password=password,
        host=host,
        database=database,
    )

    # And get the creator function from the engine
    # The creator function is stored during engine creation
    # We can call it directly to test the success path
    pool = engine.pool
    creator = pool._creator

    # When I call the creator function
    conn = creator()  # type: ignore[call-arg]

    # Then it should return the mocked connection
    assert conn == mock_connection
    # And the connector should have been called with correct parameters
    mock_connector.connect.assert_called_with(
        host,
        "pg8000",
        user=username,
        password=password,
        db=database,
    )


@patch("google_cloud_sql_postgres_sqlalchemy.create_engine.Connector")
def test_create_postgres_engine_in_cloud_sql_connection_failure(
    mock_connector_class: Mock,
) -> None:
    """Test that RuntimeError is raised when Cloud SQL connection fails.

    Note: The error is raised when attempting to use the connection,
    not during engine creation.
    """
    # Given database connection parameters
    username = "test_user"
    password = "test_password"
    host = "test-project:us-central1:test-instance"
    database = "test_db"

    # And the connector returns None (connection failure)
    mock_connector = Mock()
    mock_connector.connect.return_value = None
    mock_connector_class.return_value = mock_connector

    # When I create a Cloud SQL Postgres engine
    engine = create_postgres_engine_in_cloud_sql(
        username=username,
        password=password,
        host=host,
        database=database,
    )

    # Then the engine should be created (error happens later during connection)
    assert isinstance(engine, Engine)

    # When attempting to actually connect (simulating engine usage)
    # The engine has a creator function that will be called when a connection is needed
    # We can test this by trying to get a raw connection from the engine
    with pytest.raises(RuntimeError) as exc_info:
        # This will call the creator function internally
        engine.connect()

    assert "Failed to create Cloud SQL connection" in str(exc_info.value)
