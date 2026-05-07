"""Tests for infradex CLI."""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from infradex.cli import main

# Fake CompletedProcess returned by all subprocess.run mocks
_OK = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
_FAIL = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="err")


def _which_ok(name: str) -> str:
    """Pretend every tool is installed."""
    return f"/usr/local/bin/{name}"


class TestMainCommand:
    """Test main CLI group."""

    def test_version_flag(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.1" in result.output

    def test_help_flag(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "infrastructure-as-code" in result.output.lower()


class TestDeployCommand:
    """Test deploy command."""

    @patch("pathlib.Path.exists", return_value=True)
    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_deploy_vps_dry_run(
        self, _which: MagicMock, _run: MagicMock, _exists: MagicMock
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "vps", "--dry-run"])
        assert result.exit_code == 0, result.output
        assert "dry run" in result.output.lower()
        assert "vps" in result.output.lower()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_deploy_aws_dry_run(
        self, _which: MagicMock, _run: MagicMock, _exists: MagicMock
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "aws", "--dry-run"])
        assert result.exit_code == 0, result.output
        assert "dry run" in result.output.lower()
        assert "aws" in result.output.lower()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_deploy_gcp_dry_run(
        self, _which: MagicMock, _run: MagicMock, _exists: MagicMock
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "gcp", "--dry-run"])
        assert result.exit_code == 0, result.output
        assert "dry run" in result.output.lower()
        assert "gcp" in result.output.lower()

    @patch("pathlib.Path.exists", return_value=True)
    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_deploy_without_dry_run(
        self, _which: MagicMock, _run: MagicMock, _exists: MagicMock
    ) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "vps"])
        assert "deploying to" in result.output.lower()

    def test_deploy_invalid_target(self) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "invalid"])
        assert result.exit_code != 0
        assert "invalid value" in result.output.lower()


class TestStatusCommand:
    """Test status command."""

    @patch("subprocess.run", return_value=_FAIL)
    @patch("shutil.which", side_effect=_which_ok)
    def test_status_output(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["status"])
        assert result.exit_code == 0, result.output
        assert "dataenginex" in result.output.lower()
        assert "postgres" in result.output.lower()
        assert "redis" in result.output.lower()


class TestBackupCommand:
    """Test backup command."""

    @patch("subprocess.run", return_value=_FAIL)
    @patch("shutil.which", side_effect=_which_ok)
    def test_backup_output(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["backup"])
        # backup may succeed or fail depending on pod detection
        assert "backing up" in result.output.lower() or "error" in result.output.lower()


class TestRotateSecretsCommand:
    """Test rotate-secrets command."""

    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_rotate_secrets_output(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["rotate-secrets"])
        assert result.exit_code == 0, result.output
        assert "secret" in result.output.lower()


class TestLogsCommand:
    """Test logs command."""

    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_logs_default_tail(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["logs"])
        assert result.exit_code == 0, result.output
        assert "streaming" in result.output.lower() or "--tail=" in result.output

    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_logs_custom_tail(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "-n", "100"])
        assert result.exit_code == 0, result.output
        assert "100" in result.output

    @patch("subprocess.run", return_value=_OK)
    @patch("shutil.which", side_effect=_which_ok)
    def test_logs_tail_long_option(self, _which: MagicMock, _run: MagicMock) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "--tail", "200"])
        assert result.exit_code == 0, result.output
        assert "200" in result.output
