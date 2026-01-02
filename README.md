# Google Cloud SQL PostgreSQL SQLAlchemy

A Python library that provides utilities for creating SQLAlchemy engines that work with PostgreSQL databases, both locally and on Google Cloud SQL.

## Features

- **Simple PostgreSQL connections**: Create SQLAlchemy engines for local PostgreSQL databases
- **Google Cloud SQL support**: Seamlessly connect to Cloud SQL PostgreSQL instances using the Cloud SQL Python Connector
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

### 0.1.0 (2026-01-01)
- Initial release
- Support for local PostgreSQL connections
- Support for Google Cloud SQL connections
- Automatic connection routing based on configuration
