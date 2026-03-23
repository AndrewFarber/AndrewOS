from unittest.mock import patch

import pytest

from nix_audit.app import NixAuditApp
from nix_audit.models.database import AuditDatabase
from nix_audit.screens.audit import AuditScreen


@pytest.fixture
def mock_packages():
    return [
        {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
    ]


@pytest.fixture
def app(tmp_path, mock_packages):
    with patch("nix_audit.screens.packages.get_installed_packages") as mock_get:
        mock_get.return_value = mock_packages
        test_app = NixAuditApp()
        test_app.db = AuditDatabase(db_path=tmp_path / "test.db")
        yield test_app
        test_app.db.close()


def _mock_stream_result():
    """Return a mock coroutine for stream_claude_audit that calls on_line."""

    async def mock_stream(*_args, on_line=None, **_kwargs):
        for text in ["line 1\n", "line 2\n"]:
            if on_line:
                on_line(text)
        return {
            "risk_level": "LOW",
            "findings": [],
            "summary": "All good.",
            "report_markdown": "# Security Audit: hello 2.12.1\n\nAll good.",
        }

    return mock_stream


@pytest.mark.asyncio
async def test_audit_screen_compose(app):
    """AuditScreen composes with expected widgets."""
    with patch("nix_audit.screens.packages.get_installed_packages", return_value=[]):
        async with app.run_test() as pilot:
            await pilot.pause()
            screen = AuditScreen(
                package_name="hello",
                version="2.12.1",
                derivation_source="source",
            )
            with patch(
                "nix_audit.screens.audit.stream_claude_audit",
                side_effect=_mock_stream_result(),
            ):
                app.push_screen(screen)
                await pilot.pause()
                from textual.widgets import RichLog, Static

                assert screen.query_one("#audit-info", Static) is not None
                assert screen.query_one("#audit-log", RichLog) is not None
                assert screen.query_one("#audit-status", Static) is not None


@pytest.mark.asyncio
async def test_audit_screen_streaming(app):
    """Lines stream into RichLog and result is available for v key."""
    with patch("nix_audit.screens.packages.get_installed_packages", return_value=[]):
        async with app.run_test() as pilot:
            await pilot.pause()
            app.db.upsert_package("hello", "2.12.1")
            screen = AuditScreen(
                package_name="hello",
                version="2.12.1",
                derivation_source="source",
            )
            with patch(
                "nix_audit.screens.audit.stream_claude_audit",
                side_effect=_mock_stream_result(),
            ):
                app.push_screen(screen)
                await pilot.pause()
                await app.workers.wait_for_complete()
                await pilot.pause()

            assert screen._report is not None
            assert "Security Audit" in screen._report


@pytest.mark.asyncio
async def test_audit_screen_v_key_no_report(app):
    """Pressing v with no report shows notification."""
    with patch("nix_audit.screens.packages.get_installed_packages", return_value=[]):
        async with app.run_test() as pilot:
            await pilot.pause()
            screen = AuditScreen(
                package_name="hello",
                version="2.12.1",
                derivation_source="source",
            )

            async def mock_fail(*_args, **_kwargs):
                raise RuntimeError("test error")

            with patch(
                "nix_audit.screens.audit.stream_claude_audit",
                side_effect=mock_fail,
            ):
                app.push_screen(screen)
                await pilot.pause()
                await app.workers.wait_for_complete()
                await pilot.pause()

            # No report generated, pressing v should notify
            await pilot.press("v")
            await pilot.pause()


@pytest.mark.asyncio
async def test_audit_screen_go_back(app):
    """Pressing q pops the audit screen."""
    with patch("nix_audit.screens.packages.get_installed_packages", return_value=[]):
        async with app.run_test() as pilot:
            await pilot.pause()
            screen = AuditScreen(
                package_name="hello",
                version="2.12.1",
                derivation_source="source",
            )
            with patch(
                "nix_audit.screens.audit.stream_claude_audit",
                side_effect=_mock_stream_result(),
            ):
                app.push_screen(screen)
                await pilot.pause()
                await app.workers.wait_for_complete()
                await pilot.pause()

            await pilot.press("q")
            await pilot.pause()
            assert not isinstance(app.screen, AuditScreen)
