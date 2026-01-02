# Google Cloud SQL PostgreSQL SQLAlchemy

A Python library that provides utilities for creating SQLAlchemy engines that work with PostgreSQL databases, both locally and on Google Cloud SQL.

## Features

- **Simple PostgreSQL connections**: Create SQLAlchemy engines for local PostgreSQL databases
- **Google Cloud SQL support**: Seamlessly connect to Cloud SQL PostgreSQL instances using the Cloud SQL Python Connector
- **Cloud SQL Proxy utilities**: Cross-platform utilities for managing Cloud SQL Proxy lifecycle
- **Automatic routing**: Intelligently choose between local and Cloud SQL connections based on configuration
- **Type-safe**: Full type hints support for better IDE integration and code quality

## Installation

```bash
pip install google-cloud-sql-postgres-sqlalchemy
```

## Usage

### Local PostgreSQL Connection

```python
from google_cloud_sql_postgres_sqlalchemy import create_postgres_engine

engine = create_postgres_engine(
    username="myuser",
    password="mypassword",
    host="localhost",
    database="mydatabase",
)
```

### Google Cloud SQL Connection

```python
from google_cloud_sql_postgres_sqlalchemy import create_postgres_engine_in_cloud_sql

engine = create_postgres_engine_in_cloud_sql(
    username="myuser",
    password="mypassword",
    host="project:region:instance",  # Cloud SQL instance connection name
    database="mydatabase",
)
```

### Automatic Connection Selection

```python
from google_cloud_sql_postgres_sqlalchemy import create_database_engine

# Automatically chooses Cloud SQL if google_cloud_project_id is provided
engine = create_database_engine(
    username="myuser",
    password="mypassword",
    host="localhost",  # or Cloud SQL instance connection name
    database="mydatabase",
    google_cloud_project_id=None,  # Set to project ID to use Cloud SQL
)
```

### Using Cloud SQL Proxy (Alternative Method)

For development or testing, you can use the Cloud SQL Proxy utilities to connect to Cloud SQL through a local proxy:

```python
from google_cloud_sql_postgres_sqlalchemy import (
    cloud_sql_proxy_running,
    create_postgres_engine,
)

# Start Cloud SQL Proxy and connect through it
with cloud_sql_proxy_running(
    instance_connection_name="project:region:instance",
    port=5432,
):
    # While the proxy is running, connect as if it's a local database
    engine = create_postgres_engine(
        username="myuser",
        password="mypassword",
        host="localhost",
        database="mydatabase",
    )
    # Use the engine...
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
```

**Cross-platform proxy detection**: The `cloud_sql_proxy_running` context manager automatically detects the Cloud SQL Proxy binary path on macOS (Intel/Apple Silicon), Linux, and Windows. You can also provide an explicit path:

```python
from google_cloud_sql_postgres_sqlalchemy import get_cloud_sql_proxy_path

# Auto-detect proxy path
proxy_path = get_cloud_sql_proxy_path()
print(f"Using proxy at: {proxy_path}")

# Or specify a custom path
with cloud_sql_proxy_running(
    instance_connection_name="project:region:instance",
    port=5432,
    cloud_sql_proxy_path="/custom/path/to/cloud-sql-proxy",
):
    # ...
```

## Requirements

- Python 3.10+
- SQLAlchemy 2.0+
- pg8000 1.30+
- cloud-sql-python-connector 1.0+

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Authors

- Javad

## Changelog

### 0.2.2 (2026-01-02)
- Add comprehensive unit tests achieving 100% test coverage
- Add 13 tests for cloud_sql_proxy module covering all platforms
- Add test for successful Cloud SQL connection creation
- Update author email

### 0.2.1 (2026-01-02)
- Fix GitHub Actions publish workflow permissions
- Add comprehensive documentation for Cloud SQL Proxy utilities

### 0.2.0 (2026-01-02)
- Add cross-platform Cloud SQL Proxy utilities
- Add `cloud_sql_proxy_running()` context manager
- Add `get_cloud_sql_proxy_path()` for automatic proxy detection across macOS, Linux, and Windows

### 0.1.0 (2026-01-01)
- Initial release
- Support for local PostgreSQL connections
- Support for Google Cloud SQL connections
- Automatic connection routing based on configuration
