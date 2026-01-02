"""Utilities for working with Cloud SQL Proxy."""

import logging
import os
import platform
import re
import shutil
import subprocess
import time
from collections.abc import Generator
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def is_valid_cloud_sql_instance_name(instance_connection_name: str) -> bool:
    """
    Validate Cloud SQL instance connection name format.

    The format should be: project-id:region:instance-name

    Args:
        instance_connection_name: The instance connection name to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> is_valid_cloud_sql_instance_name("my-project:us-central1:my-instance")
        True
        >>> is_valid_cloud_sql_instance_name("invalid-format")
        False
    """
    # Pattern: project-id:region:instance-name
    # Project IDs: 6-30 chars, start with letter, letters/numbers/hyphens
    # Region: GCP region format (e.g., us-central1, northamerica-northeast1)
    # Instance name: letters, numbers, hyphens
    pattern = r"^[a-z][a-z0-9-]{5,29}:[a-z]+(-[a-z]+)*\d+:[a-z0-9-]+$"
    return bool(re.match(pattern, instance_connection_name))


def get_cloud_sql_proxy_path() -> str:
    """
    Automatically detects the cloud-sql-proxy path based on the operating system.

    Returns the path to cloud-sql-proxy executable.
    """
    # First, try to find it in PATH
    proxy_path = shutil.which("cloud-sql-proxy")
    if proxy_path:
        return proxy_path

    # Platform-specific default paths
    system = platform.system()

    if system == "Darwin":  # macOS
        # Try common Homebrew paths
        possible_paths = [
            "/opt/homebrew/bin/cloud-sql-proxy",  # Apple Silicon
            "/usr/local/bin/cloud-sql-proxy",  # Intel Mac
        ]
    elif system == "Linux":
        possible_paths = [
            "/usr/local/bin/cloud-sql-proxy",
            "/usr/bin/cloud-sql-proxy",
        ]
    elif system == "Windows":
        possible_paths = [
            (
                "C:\\Program Files\\Google\\Cloud SDK\\"
                "google-cloud-sdk\\bin\\cloud-sql-proxy.exe"
            ),
            "cloud-sql-proxy.exe",
        ]
    else:
        possible_paths = []

    # Check if any of the default paths exist
    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Fallback to just the command name (will fail if not in PATH)
    return "cloud-sql-proxy"


@contextmanager
def cloud_sql_proxy_running(
    *,
    instance_connection_name: str,
    port: int,
    cloud_sql_proxy_path: str | None = None,
) -> Generator[None]:
    """
    Context manager to run cloud-sql-proxy.

    Args:
        instance_connection_name: GCP Cloud SQL instance connection name
        port: Local port to bind the proxy to
        cloud_sql_proxy_path: Optional explicit path to cloud-sql-proxy.
                              If None, will auto-detect based on OS.
    """
    if cloud_sql_proxy_path is None:
        cloud_sql_proxy_path = get_cloud_sql_proxy_path()

    logger.info("Starting Cloud SQL Proxy...")
    logger.info("Using cloud-sql-proxy at: %s", cloud_sql_proxy_path)
    logger.info("Connecting to instance: %s on port %s", instance_connection_name, port)

    process = subprocess.Popen(
        [
            cloud_sql_proxy_path,
            f"{instance_connection_name}",
            "--port",
            f"{port}",
        ],
    )
    time.sleep(5)  # wait for proxy to start
    try:
        yield
    finally:
        process.terminate()
        process.wait()
