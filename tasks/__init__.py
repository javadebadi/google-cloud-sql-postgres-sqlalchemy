"""Tasks for the google-cloud-sql-postgres-sqlalchemy package."""

from invoke.collection import Collection

from . import code

ns = Collection()
ns.add_collection(code.ns)

__all__ = ["ns"]
