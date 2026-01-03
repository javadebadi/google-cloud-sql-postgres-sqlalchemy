# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-02

### Added
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
