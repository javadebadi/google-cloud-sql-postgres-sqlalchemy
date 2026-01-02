"""Reusable code quality tasks for Python projects."""

import webbrowser
from pathlib import Path

from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task


def _run_format(c: Context, path: str = ".") -> None:
    c.run(f"ruff format {path}")


def _run_black(c: Context, path: str = ".") -> None:
    c.run(f"black {path}")


@task(help={"path": "Path to folder to autoformat its code."})
def autoformat(c: Context, path: str = ".") -> None:
    """Lint and autofix code with ruff and black."""
    _run_black(c, path=path)
    _run_format(c, path=path)
    cmd = f"ruff check {path} --fix"
    c.run(cmd, pty=True)


@task(help={"path": "Path to folder to run ruff check on."})
def check(c: Context, path: str = ".") -> None:
    """
    Check if code is already formatted / lint-fixed.
    Fails (non-zero exit) if any issues are present.
    """
    # Ruff check only (no --fix), it will return non-zero if issues exist
    format_result = c.run(f"ruff format --diff {path}", pty=True)
    lint_result = c.run(f"ruff check {path}", pty=True)
    if (format_result and format_result.exited != 0) or (
        lint_result and lint_result.exited != 0
    ):
        print(
            "❌ Code is not properly formatted or linted. "
            "Run `invoke code.autoformat` to fix.",
        )
        exit(1)
    else:
        print("✅ Code is properly formatted and linted.")


@task(help={"path": "Path to tests or test folder."})
def mypy(c: Context, path: str = ".") -> None:
    """Run mypy type checking."""
    c.run(f"mypy {path}", pty=True)


@task(help={"path": "Path to tests or test folder."})
def ty(c: Context, path: str = ".") -> None:
    """Run ty type checking (faster alternative to mypy)."""
    c.run(f"ty check {path}", pty=True)


@task(help={"path": "Path to tests or test folder."})
def test(c: Context, path: str = "tests") -> None:
    """
    Run pytest on test suite.

    Args:
        path: Path to tests
    """
    c.run(f"pytest -vv {path} || [ $? -eq 5 ]", pty=True)


@task(help={})
def coverage(c: Context, path: str = "google_cloud_sql_postgres_sqlalchemy") -> None:
    """
    Run pytest coverage on test suite and generate HTML report.

    Args:
        path: Coverage path (default: google_cloud_sql_postgres_sqlalchemy)
    """
    c.run(f"pytest --cov={path}", pty=True)
    c.run("coverage html")


@task(help={})
def coverage_open(
    c: Context,
    path: str = "google_cloud_sql_postgres_sqlalchemy",
) -> None:
    """
    Run pytest coverage, generate HTML report, and open in browser.
    """
    coverage(c, path=path)

    # Open in default browser (cross-platform)
    report_path = Path("htmlcov/index.html").absolute()
    if report_path.exists():
        webbrowser.open(f"file://{report_path}")
    else:
        print("Coverage report not found at htmlcov/index.html")


@task(help={})
def coverage_score(
    c: Context,
    path: str = "google_cloud_sql_postgres_sqlalchemy",
) -> None:
    """Get single coverage score as percentage."""
    cmd = f"pytest --cov={path} -q 2>&1 | grep 'TOTAL' | awk '{{print $NF}}'"
    result = c.run(cmd, pty=False, hide=True)
    if result and result.stdout:
        score = result.stdout.strip()
        print(f"Coverage: {score}")
    else:
        print("Could not determine coverage score")


@task(help={"path": "Path to tests or test folder."})
def ci(c: Context, path: str = ".") -> None:
    """
    Run Continuous Integration tasks including autoformat, ty, mypy, test.
    """
    autoformat(c, path=path)
    check(c, path=path)
    ty(c, path=path)
    mypy(c, path=path)
    test(c)


@task(help={})
def clean(c: Context) -> None:
    """Remove cached folders."""
    c.run("rm -rf .mypy_cache", pty=True)
    c.run("rm -rf .pytest_cache", pty=True)
    c.run("rm -rf .ruff_cache", pty=True)
    c.run('find . -type d -name "__pycache__" -exec rm -rf {} +', pty=True)
    c.run("rm -rf htmlcov")
    c.run("rm -rf *.egg-info")
    c.run("rm -rf build")
    c.run("rm -rf dist")


# Create collection for export
ns = Collection("code")
ns.add_task(autoformat)
ns.add_task(check)
ns.add_task(mypy)
ns.add_task(ty)
ns.add_task(test)
ns.add_task(ci)
ns.add_task(clean)
ns.add_task(coverage)
ns.add_task(coverage_open)
ns.add_task(coverage_score)

__all__ = ["ns"]
