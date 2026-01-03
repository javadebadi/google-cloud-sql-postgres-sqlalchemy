# Contributing

Thank you for considering contributing to this project!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy.git
cd google-cloud-sql-postgres-sqlalchemy
```

2. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:
```bash
uv sync --dev
```

## Running Tests

Run all tests:
```bash
uv run invoke code.test
```

Run tests with coverage:
```bash
uv run invoke code.coverage-xml
```

## Code Quality

Run all CI checks (format, lint, type check, security, complexity, tests):
```bash
uv run invoke code.ci
```

Format code:
```bash
uv run invoke code.autoformat
```

Type check:
```bash
uv run invoke code.mypy
```

Security scan:
```bash
uv run invoke code.security
```

## Documentation

Build documentation:
```bash
uv run invoke code.docs
```

Serve documentation locally:
```bash
uv run invoke code.docs-serve
```

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `uv run invoke code.ci` to ensure all checks pass
5. Submit a pull request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
