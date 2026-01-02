"""Tests for the create_engine module."""

import os
from unittest.mock import Mock, patch

import pytest
from sqlalchemy import Engine, text

from google_cloud_sql_postgres_sqlalchemy.create_engine import (
    create_database_engine,
    create_postgres_engine,
    create_postgres_engine_in_cloud_sql,
    create_sqlalchemy_url,
)


def test_create_sqlalchemy_url_without_port() -> None:
    """Test creating SQLAlchemy URL without port."""
    # Given database connection parameters without port
    url = create_sqlalchemy_url(
        username="testuser",
        password="testpass",
        host="localhost",
        database="testdb",
    )

    # Then URL should be formatted correctly without port
    assert url == "postgresql+pg8000://testuser:testpass@localhost/testdb"


def test_create_sqlalchemy_url_with_port() -> None:
    """Test creating SQLAlchemy URL with port."""
    # Given database connection parameters with port
    url = create_sqlalchemy_url(
        username="testuser",
        password="testpass",
        host="localhost",
        database="testdb",
        port=5432,
    )

    # Then URL should be formatted correctly with port
    assert url == "postgresql+pg8000://testuser:testpass@localhost:5432/testdb"


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


def test_create_postgres_engine_with_custom_pool_settings() -> None:
    """Test creating a Postgres engine with custom pool configuration."""
    # Given database connection parameters and custom pool settings
    username = "test_user"
    password = "test_password"
    host = "localhost"
    database = "test_db"
    pool_size = 50
    max_overflow = 20
    pool_timeout = 60
    pool_recycle = 7200

    # When I create a Postgres engine with custom pool settings
    engine = create_postgres_engine(
        username=username,
        password=password,
        host=host,
        database=database,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
    )

    # Then the engine should have the custom pool settings
    assert isinstance(engine, Engine)
    assert engine.pool.size() == pool_size  # type: ignore
    assert engine.pool._max_overflow == max_overflow  # type: ignore
    assert engine.pool._timeout == pool_timeout  # type: ignore
    assert engine.pool._recycle == pool_recycle


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


def test_create_postgres_engine_in_cloud_sql_invalid_instance_name() -> None:
    """Test that ValueError is raised for invalid instance connection name."""
    # Given database connection parameters with invalid instance name
    username = "test_user"
    password = "test_password"
    invalid_host = "invalid-format"  # Missing region and instance
    database = "test_db"

    # When I try to create a Cloud SQL Postgres engine with invalid name
    # Then it should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        create_postgres_engine_in_cloud_sql(
            username=username,
            password=password,
            host=invalid_host,
            database=database,
        )

    # And the error message should be helpful
    assert "Invalid Cloud SQL instance connection name" in str(exc_info.value)
    assert "project-id:region:instance-name" in str(exc_info.value)


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


# ============================================================================
# Integration Tests - Use Real PostgreSQL Database
# ============================================================================


def get_postgres_config() -> dict[str, str | int] | None:
    """Get PostgreSQL configuration from environment variables.

    Returns:
        Dict with connection parameters if all env vars are set, None otherwise.
    """
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")

    if all([host, port, user, password, database]):
        return {
            "host": str(host),
            "port": int(port),  # type: ignore[arg-type]
            "username": str(user),
            "password": str(password),
            "database": str(database),
        }
    return None


@pytest.mark.skipif(
    get_postgres_config() is None,
    reason="PostgreSQL environment variables not set",
)
def test_create_postgres_engine_integration() -> None:
    """Integration test: Create engine and connect to real PostgreSQL."""
    # Given PostgreSQL is available via environment variables
    config = get_postgres_config()
    assert config is not None

    # When I create a PostgreSQL engine
    engine = create_postgres_engine(
        username=config["username"],  # type: ignore[arg-type]
        password=config["password"],  # type: ignore[arg-type]
        host=config["host"],  # type: ignore[arg-type]
        database=config["database"],  # type: ignore[arg-type]
    )

    # Then the engine should be created successfully
    assert isinstance(engine, Engine)

    # And I should be able to connect and execute a query
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as num"))
        row = result.fetchone()
        assert row is not None
        assert row[0] == 1


@pytest.mark.skipif(
    get_postgres_config() is None,
    reason="PostgreSQL environment variables not set",
)
def test_create_sqlalchemy_url_integration() -> None:
    """Integration test: URL string works with real PostgreSQL."""
    # Given PostgreSQL is available via environment variables
    config = get_postgres_config()
    assert config is not None

    # When I create a SQLAlchemy URL string
    url = create_sqlalchemy_url(
        username=config["username"],  # type: ignore[arg-type]
        password=config["password"],  # type: ignore[arg-type]
        host=config["host"],  # type: ignore[arg-type]
        database=config["database"],  # type: ignore[arg-type]
        port=config["port"],  # type: ignore[arg-type]
    )

    # Then the URL should contain all connection parameters
    assert str(config["username"]) in url
    assert str(config["host"]) in url
    assert str(config["database"]) in url

    # And I should be able to create an engine and connect with it
    from sqlalchemy import create_engine as sa_create_engine

    engine = sa_create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        row = result.fetchone()
        assert row is not None
        assert "PostgreSQL" in row[0]


@pytest.mark.skipif(
    get_postgres_config() is None,
    reason="PostgreSQL environment variables not set",
)
def test_connection_pool_integration() -> None:
    """Integration test: Connection pool works with real PostgreSQL."""
    # Given PostgreSQL is available and custom pool settings
    config = get_postgres_config()
    assert config is not None

    pool_size = 5
    max_overflow = 3

    # When I create an engine with custom pool settings
    engine = create_postgres_engine(
        username=config["username"],  # type: ignore[arg-type]
        password=config["password"],  # type: ignore[arg-type]
        host=config["host"],  # type: ignore[arg-type]
        database=config["database"],  # type: ignore[arg-type]
        pool_size=pool_size,
        max_overflow=max_overflow,
    )

    # Then the pool should have the correct settings
    assert engine.pool.size() == pool_size  # type: ignore[attr-defined]
    assert engine.pool._max_overflow == max_overflow  # type: ignore[attr-defined]

    # And I should be able to use multiple connections from the pool
    connections = []
    try:
        # Get multiple connections from the pool
        for _ in range(pool_size):
            conn = engine.connect()
            connections.append(conn)
            # Verify each connection works
            result = conn.execute(text("SELECT 1"))
            assert result.fetchone()[0] == 1  # type: ignore[index]
    finally:
        # Clean up connections
        for conn in connections:
            conn.close()


@pytest.mark.skipif(
    get_postgres_config() is None,
    reason="PostgreSQL environment variables not set",
)
def test_create_database_engine_integration_without_cloud_sql() -> None:
    """Integration test: create_database_engine works without Cloud SQL."""
    # Given PostgreSQL is available and no google_cloud_project_id
    config = get_postgres_config()
    assert config is not None

    # When I create a database engine without Cloud SQL
    engine = create_database_engine(
        username=config["username"],  # type: ignore[arg-type]
        password=config["password"],  # type: ignore[arg-type]
        host=config["host"],  # type: ignore[arg-type]
        database=config["database"],  # type: ignore[arg-type]
        google_cloud_project_id=None,
    )

    # Then the engine should work with real PostgreSQL
    assert isinstance(engine, Engine)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database()"))
        row = result.fetchone()
        assert row is not None
        assert row[0] == config["database"]
