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
        assert "0.1.0" in result.output

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
        """Test deploy without dry-run flag."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "vps"])
        assert result.exit_code == 0
        assert "deployment complete" in result.output.lower()
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
        """Test backup command output."""
        runner = CliRunner()
        result = runner.invoke(main, ["backup"])
        assert result.exit_code == 0
        assert "backup" in result.output.lower()


class TestRotateSecretsCommand:
    """Test rotate-secrets command."""

    def test_rotate_secrets_output(self) -> None:
        """Test rotate-secrets command output."""
        runner = CliRunner()
        result = runner.invoke(main, ["rotate-secrets"])
        assert result.exit_code == 0
        assert "secret" in result.output.lower()


class TestLogsCommand:
    """Test logs command."""

    def test_logs_default_tail(self) -> None:
        """Test logs command with default tail."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs"])
        assert result.exit_code == 0
        assert "50" in result.output or "fetching" in result.output.lower()

    def test_logs_custom_tail(self) -> None:
        """Test logs command with custom tail."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "-n", "100"])
        assert result.exit_code == 0
        assert "100" in result.output

    def test_logs_tail_long_option(self) -> None:
        """Test logs command with --tail option."""
        runner = CliRunner()
        result = runner.invoke(main, ["logs", "--tail", "200"])
        assert result.exit_code == 0
        assert "200" in result.output
