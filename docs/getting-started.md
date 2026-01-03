# Getting Started

## Installation

Install the package using pip:

```bash
pip install google-cloud-sql-postgres-sqlalchemy
```

## Basic Usage

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

## Next Steps

- See the [API Reference](api/create_engine.md) for detailed documentation
- Check out [Examples](examples.md) for more usage patterns
