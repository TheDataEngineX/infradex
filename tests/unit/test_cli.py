"""Tests for infradex CLI."""

from __future__ import annotations

from click.testing import CliRunner

from infradex.cli import main


class TestMainCommand:
    """Test main CLI group."""

    def test_version_flag(self) -> None:
        """Test --version flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.1" in result.output

    def test_help_flag(self) -> None:
        """Test --help flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "infrastructure-as-code" in result.output.lower()


class TestDeployCommand:
    """Test deploy command."""

    def test_deploy_vps_dry_run(self) -> None:
        """Test deploy to VPS with dry-run flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "vps", "--dry-run"])
        assert result.exit_code == 0
        assert "dry run" in result.output.lower()
        assert "vps" in result.output.lower()

    def test_deploy_aws_dry_run(self) -> None:
        """Test deploy to AWS with dry-run flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "aws", "--dry-run"])
        assert result.exit_code == 0
        assert "dry run" in result.output.lower()
        assert "aws" in result.output.lower()

    def test_deploy_gcp_dry_run(self) -> None:
        """Test deploy to GCP with dry-run flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "gcp", "--dry-run"])
        assert result.exit_code == 0
        assert "dry run" in result.output.lower()
        assert "gcp" in result.output.lower()

    def test_deploy_without_dry_run(self) -> None:
        """Deploy without --dry-run prints intent then raises NotImplementedError."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "vps"])
        assert result.exit_code != 0
        assert "deploying to" in result.output.lower()

    def test_deploy_invalid_target(self) -> None:
        """Test deploy with invalid target."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "invalid"])
        assert result.exit_code != 0
        assert "invalid value" in result.output.lower()


class TestStatusCommand:
    """Test status command."""

    def test_status_output(self) -> None:
        """Test status command output."""
        runner = CliRunner()
        result = runner.invoke(main, ["status"])
        assert result.exit_code == 0
        assert "cluster status" in result.output.lower()
        assert "dataenginex" in result.output.lower()
        assert "postgres" in result.output.lower()
        assert "redis" in result.output.lower()


class TestBackupCommand:
    """Test backup command."""

    def test_backup_output(self) -> None:
        """Backup prints intent then raises NotImplementedError."""
        runner = CliRunner()
        result = runner.invoke(main, ["backup"])
        assert result.exit_code != 0
        assert "backing up" in result.output.lower()


class TestRotateSecretsCommand:
    """Test rotate-secrets command."""

    def test_rotate_secrets_output(self) -> None:
        """rotate-secrets prints intent then raises NotImplementedError."""
        runner = CliRunner()
        result = runner.invoke(main, ["rotate-secrets"])
        assert result.exit_code != 0
        assert "secret" in result.output.lower()


class TestLogsCommand:
    """Test logs command."""

    def test_logs_default_tail(self) -> None:
        """logs prints intent then raises NotImplementedError ."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs"])
        assert result.exit_code != 0
        assert "50" in result.output or "fetching" in result.output.lower()

    def test_logs_custom_tail(self) -> None:
        """logs with -n passes value through before raising NotImplementedError."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "-n", "100"])
        assert result.exit_code != 0
        assert "100" in result.output

    def test_logs_tail_long_option(self) -> None:
        """logs with --tail passes value through before raising NotImplementedError."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "--tail", "200"])
        assert result.exit_code != 0
        assert "200" in result.output
