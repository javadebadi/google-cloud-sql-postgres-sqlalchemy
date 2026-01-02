[![codecov](https://codecov.io/gh/javadebadi/google-cloud-sql-postgres-sqlalchemy/branch/main/graph/badge.svg)](https://codecov.io/gh/javadebadi/google-cloud-sql-postgres-sqlalchemy)
[![PyPI version](https://badge.fury.io/py/google-cloud-sql-postgres-sqlalchemy.svg)](https://badge.fury.io/py/google-cloud-sql-postgres-sqlalchemy)
[![Python Versions](https://img.shields.io/pypi/pyversions/google-cloud-sql-postgres-sqlalchemy.svg)](https://pypi.org/project/google-cloud-sql-postgres-sqlalchemy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/workflows/Continuous%20Integration/badge.svg)](https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/actions)
[![Downloads](https://pepy.tech/badge/google-cloud-sql-postgres-sqlalchemy)](https://pepy.tech/project/google-cloud-sql-postgres-sqlalchemy)

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

### Creating SQLAlchemy URL Strings

If you need to generate a SQLAlchemy connection URL string (e.g., for configuration files or frameworks):

```python
from google_cloud_sql_postgres_sqlalchemy import create_sqlalchemy_url

# Without port
url = create_sqlalchemy_url(
    username="myuser",
    password="mypassword",
    host="localhost",
    database="mydatabase",
)
# Returns: 'postgresql+pg8000://myuser:mypassword@localhost/mydatabase'

# With port
url = create_sqlalchemy_url(
    username="myuser",
    password="mypassword",
    host="localhost",
    database="mydatabase",
    port=5432,
)
# Returns: 'postgresql+pg8000://myuser:mypassword@localhost:5432/mydatabase'
```

### Connection Pool Configuration

All engine creation functions support connection pool configuration:

```python
engine = create_postgres_engine(
    username="myuser",
    password="mypassword",
    host="localhost",
    database="mydatabase",
    pool_size=20,          # Number of connections to maintain (default: 20)
    max_overflow=10,       # Additional connections beyond pool_size (default: 10)
    pool_timeout=30,       # Seconds to wait for connection (default: 30)
    pool_recycle=3600,     # Recycle connections after N seconds (default: 3600)
)
```

**Pool Parameters**:
- `pool_size`: Number of connections to keep open. Default is 20 for production use.
- `max_overflow`: Maximum number of connections that can be created beyond `pool_size`. Total connections = pool_size + max_overflow.
- `pool_timeout`: Seconds to wait before giving up on getting a connection from the pool.
- `pool_recycle`: Number of seconds after which a connection is automatically recycled. Helps prevent stale connections.

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

### Configuring Logging

The library uses Python's standard `logging` module. To see Cloud SQL Proxy startup messages:

```python
import logging

# Configure logging to see INFO messages from the library
logging.basicConfig(level=logging.INFO)

# Or configure only for this library
logging.getLogger('google_cloud_sql_postgres_sqlalchemy').setLevel(logging.INFO)
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

### 1.0.0 (2026-01-02)
- Support for local PostgreSQL connections
- Support for Google Cloud SQL connections using Cloud SQL Python Connector
- Automatic connection routing based on configuration
- Cross-platform Cloud SQL Proxy utilities
- `cloud_sql_proxy_running()` context manager for managing proxy lifecycle
- `get_cloud_sql_proxy_path()` for automatic proxy detection across macOS, Linux, and Windows
- `create_sqlalchemy_url()` utility for generating connection URL strings
- Validation for Cloud SQL instance connection names
- Connection pool configuration (pool_size, max_overflow, pool_timeout, pool_recycle)
- Structured logging with Python's logging module
- Comprehensive unit tests achieving 100% code coverage
- Full type hints support
