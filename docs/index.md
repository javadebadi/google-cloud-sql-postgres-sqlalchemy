# Google Cloud SQL PostgreSQL SQLAlchemy

[![codecov](https://codecov.io/gh/javadebadi/google-cloud-sql-postgres-sqlalchemy/branch/main/graph/badge.svg)](https://codecov.io/gh/javadebadi/google-cloud-sql-postgres-sqlalchemy)
[![PyPI version](https://badge.fury.io/py/google-cloud-sql-postgres-sqlalchemy.svg)](https://badge.fury.io/py/google-cloud-sql-postgres-sqlalchemy)
[![Python Versions](https://img.shields.io/pypi/pyversions/google-cloud-sql-postgres-sqlalchemy.svg)](https://pypi.org/project/google-cloud-sql-postgres-sqlalchemy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/workflows/Continuous%20Integration/badge.svg)](https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/actions)
[![Downloads](https://img.shields.io/pypi/dm/google-cloud-sql-postgres-sqlalchemy)](https://pypi.org/project/google-cloud-sql-postgres-sqlalchemy/)

A Python library that provides utilities for creating SQLAlchemy engines that work with PostgreSQL databases, both locally and on Google Cloud SQL.

## Features

- **Simple PostgreSQL connections**: Create SQLAlchemy engines for local PostgreSQL databases
- **Google Cloud SQL support**: Seamlessly connect to Cloud SQL PostgreSQL instances using the Cloud SQL Python Connector
- **Cloud SQL Proxy utilities**: Cross-platform utilities for managing Cloud SQL Proxy lifecycle
- **Automatic routing**: Intelligently choose between local and Cloud SQL connections based on configuration
- **Type-safe**: Full type hints support for better IDE integration and code quality
- **100% test coverage**: Comprehensive test suite with both unit and integration tests

## Quick Start

Install the package:

```bash
pip install google-cloud-sql-postgres-sqlalchemy
```

Create a PostgreSQL engine:

```python
from google_cloud_sql_postgres_sqlalchemy import create_postgres_engine

engine = create_postgres_engine(
    username="myuser",
    password="mypassword",
    host="localhost",
    database="mydatabase",
)
```

## Documentation

- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api/create_engine.md) - Detailed API documentation
- [Examples](examples.md) - Common usage patterns

## Requirements

- Python 3.10+
- SQLAlchemy 2.0+
- pg8000 1.30+
- cloud-sql-python-connector 1.0+

## License

MIT License - see LICENSE file for details.
