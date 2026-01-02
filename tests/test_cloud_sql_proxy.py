"""Tests for the cloud_sql_proxy module."""

from unittest.mock import Mock, patch

import pytest

from google_cloud_sql_postgres_sqlalchemy import (
    cloud_sql_proxy_running,
    get_cloud_sql_proxy_path,
    is_valid_cloud_sql_instance_name,
)


class TestIsValidCloudSqlInstanceName:
    """Tests for is_valid_cloud_sql_instance_name function."""

    def test_valid_instance_names(self) -> None:
        """Test valid Cloud SQL instance connection names."""
        # Given valid instance connection names
        valid_names = [
            "my-project:us-central1:my-instance",
            "test-project:europe-west1:db-instance",
            "prod123:asia-east1:database-1",
            "project-a:us-west2:instance-b",
            "myapp01:northamerica-northeast1:postgres-db",
        ]

        # When I validate each name
        # Then all should be valid
        for name in valid_names:
            assert is_valid_cloud_sql_instance_name(name), (
                f"Expected {name} to be valid"
            )

    def test_invalid_instance_names(self) -> None:
        """Test invalid Cloud SQL instance connection names."""
        # Given invalid instance connection names
        invalid_names = [
            "invalid",  # Missing colons
            "project:region",  # Missing instance name
            "project:us-central1",  # Missing instance name
            ":us-central1:instance",  # Missing project
            "project::instance",  # Missing region
            "Project:us-central1:instance",  # Uppercase in project
            "project:US-CENTRAL1:instance",  # Uppercase in region
            "project:us-central1:Instance",  # Uppercase in instance
            "123project:us-central1:instance",  # Project starts with number
            "pr:us-central1:instance",  # Project too short (< 6 chars)
            "a" * 31 + ":us-central1:instance",  # Project too long (> 30 chars)
            "project:invalid-region:instance",  # Invalid region format
            "project:us-central:instance",  # Missing number in region
            "project:us-1:instance",  # Invalid region format
        ]

        # When I validate each name
        # Then all should be invalid
        for name in invalid_names:
            assert not is_valid_cloud_sql_instance_name(
                name,
            ), f"Expected {name} to be invalid"

    def test_edge_cases(self) -> None:
        """Test edge cases for instance name validation."""
        # Given edge case instance names
        # Minimum valid project name (6 chars)
        assert is_valid_cloud_sql_instance_name("abcdef:us-central1:instance")

        # Maximum valid project name (30 chars)
        assert is_valid_cloud_sql_instance_name(
            "a" + "b" * 28 + "c:us-central1:instance",
        )

        # Instance name with hyphens
        assert is_valid_cloud_sql_instance_name("project:us-central1:my-db-001")

        # Empty string
        assert not is_valid_cloud_sql_instance_name("")

        # Only colons
        assert not is_valid_cloud_sql_instance_name("::")


class TestGetCloudSqlProxyPath:
    """Tests for get_cloud_sql_proxy_path function."""

    @patch("shutil.which")
    def test_found_in_path(self, mock_which: Mock) -> None:
        """Test when cloud-sql-proxy is found in PATH."""
        # Given cloud-sql-proxy is in PATH
        expected_path = "/usr/bin/cloud-sql-proxy"
        mock_which.return_value = expected_path

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the PATH location
        assert result == expected_path
        mock_which.assert_called_once_with("cloud-sql-proxy")

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_macos_apple_silicon(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on macOS Apple Silicon."""
        # Given macOS system and proxy not in PATH
        mock_which.return_value = None
        mock_system.return_value = "Darwin"
        # Apple Silicon path exists
        mock_exists.side_effect = (
            lambda path: path == "/opt/homebrew/bin/cloud-sql-proxy"
        )

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the Apple Silicon Homebrew path
        assert result == "/opt/homebrew/bin/cloud-sql-proxy"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_macos_intel(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on macOS Intel."""
        # Given macOS system and proxy not in PATH
        mock_which.return_value = None
        mock_system.return_value = "Darwin"
        # Intel Mac path exists (Apple Silicon path doesn't)
        mock_exists.side_effect = lambda path: path == "/usr/local/bin/cloud-sql-proxy"

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the Intel Mac path
        assert result == "/usr/local/bin/cloud-sql-proxy"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_linux(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on Linux."""
        # Given Linux system and proxy not in PATH
        mock_which.return_value = None
        mock_system.return_value = "Linux"
        # First Linux path exists
        mock_exists.side_effect = lambda path: path == "/usr/local/bin/cloud-sql-proxy"

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the Linux path
        assert result == "/usr/local/bin/cloud-sql-proxy"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_linux_alternative_path(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on Linux with alternative path."""
        # Given Linux system and proxy not in PATH
        mock_which.return_value = None
        mock_system.return_value = "Linux"
        # Second Linux path exists
        mock_exists.side_effect = lambda path: path == "/usr/bin/cloud-sql-proxy"

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the alternative Linux path
        assert result == "/usr/bin/cloud-sql-proxy"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_windows(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on Windows."""
        # Given Windows system and proxy not in PATH
        mock_which.return_value = None
        mock_system.return_value = "Windows"
        # Windows Cloud SDK path exists
        expected_path = (
            "C:\\Program Files\\Google\\Cloud SDK\\"
            "google-cloud-sdk\\bin\\cloud-sql-proxy.exe"
        )
        mock_exists.side_effect = lambda path: path == expected_path

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the Windows Cloud SDK path
        assert result == expected_path

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_windows_current_directory(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on Windows in current directory."""
        # Given Windows system and proxy not in PATH or Cloud SDK
        mock_which.return_value = None
        mock_system.return_value = "Windows"
        # Current directory path exists
        mock_exists.side_effect = lambda path: path == "cloud-sql-proxy.exe"

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the current directory exe
        assert result == "cloud-sql-proxy.exe"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_fallback_to_command_name(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test fallback when proxy is not found anywhere."""
        # Given no proxy found anywhere
        mock_which.return_value = None
        mock_system.return_value = "Linux"
        mock_exists.return_value = False

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the command name as fallback
        assert result == "cloud-sql-proxy"

    @patch("platform.system")
    @patch("os.path.exists")
    @patch("shutil.which")
    def test_unknown_platform(
        self,
        mock_which: Mock,
        mock_exists: Mock,
        mock_system: Mock,
    ) -> None:
        """Test proxy detection on unknown platform."""
        # Given unknown platform
        mock_which.return_value = None
        mock_system.return_value = "UnknownOS"
        mock_exists.return_value = False

        # When I get the proxy path
        result = get_cloud_sql_proxy_path()

        # Then it should return the command name as fallback
        assert result == "cloud-sql-proxy"


class TestCloudSqlProxyRunning:
    """Tests for cloud_sql_proxy_running context manager."""

    @patch("subprocess.Popen")
    @patch("time.sleep")
    @patch(
        "google_cloud_sql_postgres_sqlalchemy.cloud_sql_proxy.get_cloud_sql_proxy_path",
    )
    def test_starts_and_stops_proxy(
        self,
        mock_get_path: Mock,
        mock_sleep: Mock,
        mock_popen: Mock,
    ) -> None:
        """Test that proxy starts and stops correctly."""
        # Given a proxy path and mock process
        mock_get_path.return_value = "/usr/bin/cloud-sql-proxy"
        mock_process = Mock()
        mock_popen.return_value = mock_process

        # When I use the context manager
        with cloud_sql_proxy_running(
            instance_connection_name="project:region:instance",
            port=5432,
        ):
            # Then the proxy should be started
            mock_popen.assert_called_once_with(
                [
                    "/usr/bin/cloud-sql-proxy",
                    "project:region:instance",
                    "--port",
                    "5432",
                ],
            )
            mock_sleep.assert_called_once_with(5)

        # And the proxy should be terminated when exiting context
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_uses_custom_proxy_path(
        self,
        mock_sleep: Mock,
        mock_popen: Mock,
    ) -> None:
        """Test using a custom proxy path."""
        # Given a custom proxy path
        custom_path = "/custom/path/cloud-sql-proxy"
        mock_process = Mock()
        mock_popen.return_value = mock_process

        # When I use the context manager with custom path
        with cloud_sql_proxy_running(
            instance_connection_name="project:region:instance",
            port=5433,
            cloud_sql_proxy_path=custom_path,
        ):
            # Then it should use the custom path
            mock_popen.assert_called_once_with(
                [
                    custom_path,
                    "project:region:instance",
                    "--port",
                    "5433",
                ],
            )

        # And cleanup should still happen
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    @patch("subprocess.Popen")
    @patch("time.sleep")
    @patch(
        "google_cloud_sql_postgres_sqlalchemy.cloud_sql_proxy.get_cloud_sql_proxy_path",
    )
    def test_cleanup_on_exception(
        self,
        mock_get_path: Mock,
        mock_sleep: Mock,
        mock_popen: Mock,
    ) -> None:
        """Test that proxy is cleaned up even when exception occurs."""
        # Given a proxy that starts successfully
        mock_get_path.return_value = "/usr/bin/cloud-sql-proxy"
        mock_process = Mock()
        mock_popen.return_value = mock_process

        # When an exception occurs inside the context
        with (
            pytest.raises(ValueError),
            cloud_sql_proxy_running(
                instance_connection_name="project:region:instance",
                port=5432,
            ),
        ):
            raise ValueError("Test exception")

        # Then the proxy should still be terminated
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    @patch("subprocess.Popen")
    @patch("time.sleep")
    @patch(
        "google_cloud_sql_postgres_sqlalchemy.cloud_sql_proxy.get_cloud_sql_proxy_path",
    )
    @patch("google_cloud_sql_postgres_sqlalchemy.cloud_sql_proxy.logger")
    def test_logs_startup_messages(
        self,
        mock_logger: Mock,
        mock_get_path: Mock,
        mock_sleep: Mock,
        mock_popen: Mock,
    ) -> None:
        """Test that startup messages are logged."""
        # Given a proxy path
        proxy_path = "/usr/bin/cloud-sql-proxy"
        mock_get_path.return_value = proxy_path
        mock_process = Mock()
        mock_popen.return_value = mock_process

        # When I use the context manager
        with cloud_sql_proxy_running(
            instance_connection_name="my-project:us-central1:my-instance",
            port=5432,
        ):
            pass

        # Then startup messages should be logged
        assert mock_logger.info.call_count == 3
        mock_logger.info.assert_any_call("Starting Cloud SQL Proxy...")
        mock_logger.info.assert_any_call("Using cloud-sql-proxy at: %s", proxy_path)
        mock_logger.info.assert_any_call(
            "Connecting to instance: %s on port %s",
            "my-project:us-central1:my-instance",
            5432,
        )
