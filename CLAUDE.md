# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python library that provides SQLAlchemy engine utilities for PostgreSQL databases, with special support for Google Cloud SQL. It offers three main engine creation functions with automatic routing between local and Cloud SQL connections.

## Core Architecture

### Module Structure

- `google_cloud_sql_postgres_sqlalchemy/create_engine.py`: Core engine creation logic
  - `create_postgres_engine()`: Local PostgreSQL connections using standard pg8000 driver
  - `create_postgres_engine_in_cloud_sql()`: Cloud SQL connections using google.cloud.sql.connector with a custom creator function
  - `create_database_engine()`: Intelligent router that switches between local/Cloud SQL based on `google_cloud_project_id` parameter

- `google_cloud_sql_postgres_sqlalchemy/cloud_sql_proxy.py`: Cross-platform Cloud SQL Proxy utilities
  - `get_cloud_sql_proxy_path()`: Auto-detects proxy binary path across macOS (Intel/Apple Silicon), Linux, and Windows
  - `cloud_sql_proxy_running()`: Context manager for proxy lifecycle management

### Key Design Patterns

**Connection Strategy**: The library uses SQLAlchemy's `creator` parameter for Cloud SQL connections. Instead of a standard connection URL, `create_postgres_engine_in_cloud_sql()` provides a custom `get_cloud_sql_connector()` function that returns pg8000 connections via the Cloud SQL Python Connector.

**Routing Logic**: `create_database_engine()` acts as a facade that selects the appropriate engine type based on the presence of `google_cloud_project_id`. This allows users to switch between local development and Cloud SQL production by changing a single parameter.

## Development Commands

### Task Runner (Invoke)

This project uses [Invoke](https://www.pyinvoke.org/) for task management. All commands are in `tasks/code.py`:

```bash
# Format and lint code
invoke code.autoformat

# Check formatting/linting (CI mode - fails on issues)
invoke code.check

# Type checking
invoke code.ty          # Fast type checking with ty
invoke code.mypy        # Strict type checking with mypy

# Run tests
invoke code.test                    # Run all tests
pytest tests/test_create_engine.py  # Run specific test file
pytest -k test_name                 # Run specific test

# Coverage
invoke code.coverage                # Generate coverage report
invoke code.coverage-open           # Generate and open in browser
invoke code.coverage-score          # Get coverage percentage

# Full CI suite
invoke code.ci          # Runs: autoformat, check, ty, mypy, test

# Clean artifacts
invoke code.clean       # Remove cache folders and build artifacts
```

### Direct Tool Usage

```bash
# Linting and formatting
ruff format .                    # Format code
ruff check . --fix               # Lint and autofix
black .                          # Format with black

# Type checking
mypy .                           # Strict type checking (configured in pyproject.toml)
ty check .                       # Fast type checking

# Testing
pytest                           # Run all tests
pytest -vv                       # Verbose output
pytest --cov=google_cloud_sql_postgres_sqlalchemy  # With coverage
```

### Building and Publishing

```bash
# Build package locally
python -m build

# Publishing is automated via GitHub Actions
# Push a version tag to trigger the publish workflow:
git tag v0.3.0
git push origin v0.3.0

# The workflow will:
# 1. Validate tag version matches pyproject.toml
# 2. Run full CI suite (autoformat, type checks, tests)
# 3. Build the package
# 4. Publish to Test PyPI (with --skip-existing)
# 5. Publish to PyPI
# 6. Create GitHub Release with auto-generated notes
```

## Type Safety and Code Quality

- **Strict mypy configuration**: All code must have type annotations (`disallow_untyped_defs = true`)
- **Ruff linting**: Enforces import sorting, type annotations (ANN), pyupgrade (UP), bugbear (B), and more
- **Test style**: Uses Given-When-Then comment structure in tests (see `tests/test_create_engine.py`)
- **Mocking**: Cloud SQL Connector is mocked in tests using `@patch` decorator

## Important Constraints

- Python 3.10+ required
- SQLAlchemy 2.0+ only (not compatible with 1.x)
- pg8000 is the required PostgreSQL driver (not psycopg2)
- Cloud SQL Connector must use pg8000 dialect
- All type annotations are mandatory (enforced by mypy strict mode)
