# Examples

## Creating a SQLAlchemy URL String

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

## Using Cloud SQL Proxy

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

## Configuring Logging

```python
import logging

# Configure logging to see INFO messages from the library
logging.basicConfig(level=logging.INFO)

# Or configure only for this library
logging.getLogger('google_cloud_sql_postgres_sqlalchemy').setLevel(logging.INFO)
```

## Connection Pool Configuration

```python
from google_cloud_sql_postgres_sqlalchemy import create_postgres_engine

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

## Instance Name Validation

```python
from google_cloud_sql_postgres_sqlalchemy import is_valid_cloud_sql_instance_name

# Valid instance names
is_valid_cloud_sql_instance_name("my-project:us-central1:my-instance")  # True

# Invalid instance names
is_valid_cloud_sql_instance_name("invalid-format")  # False
is_valid_cloud_sql_instance_name("project:instance")  # False (missing region)
```
