from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.app import NixAuditApp
from nix_audit.models.database import AuditDatabase


@pytest.fixture
def mock_packages():
    return [
        {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
        {"name": "hello", "version": "2.12.1", "store_path": "/nix/store/def-hello-2.12.1"},
    ]


@pytest.fixture
def app(tmp_path, mock_packages):
    """Create app with mocked nix service and temp database."""
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = mock_packages
        test_app = NixAuditApp()
        test_app.db = AuditDatabase(db_path=tmp_path / "test.db")
        yield test_app
        test_app.db.close()


@pytest.mark.asyncio
async def test_app_starts(app):
    async with app.run_test() as _pilot:
        assert app.title == "nix-audit"


@pytest.mark.asyncio
async def test_packages_screen_loads(app):
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = [
            {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
            {"name": "hello", "version": "2.12.1", "store_path": "/nix/store/def-hello-2.12.1"},
        ]
        async with app.run_test() as pilot:
            await pilot.pause()
            # Table should exist
            from nix_audit.screens.packages import PackagesScreen

            screen = app.screen
            assert isinstance(screen, PackagesScreen)


@pytest.mark.asyncio
async def test_vim_keys_j_k(app):
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = [
            {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
            {"name": "hello", "version": "2.12.1", "store_path": "/nix/store/def-hello-2.12.1"},
        ]
        async with app.run_test() as pilot:
            await pilot.pause()
            # Press j to move down
            await pilot.press("j")
            await pilot.pause()


@pytest.mark.asyncio
async def test_quit_key(app):
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = []
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("q")


@pytest.mark.asyncio
async def test_detail_save_source(app):
    """Press s on detail screen triggers save worker."""
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = [
            {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
        ]
        async with app.run_test() as pilot:
            await pilot.pause()
            # Navigate to detail screen
            app.db.upsert_package("git", "2.43.0", "/nix/store/abc-git-2.43.0")
            from nix_audit.screens.detail import DetailScreen

            app.push_screen(DetailScreen("git"))
            await pilot.pause()

            # Mock save_derivation_files to return a fake list
            with patch(
                "nix_audit.screens.detail.save_derivation_files",
                new_callable=AsyncMock,
                return_value=None,
            ):
                await pilot.press("s")
                await pilot.pause()
                # Should not crash; status should update
                from textual.widgets import Static

                status = app.screen.query_one("#action-status", Static)
                assert status is not None


@pytest.mark.asyncio
async def test_detail_open_editor_no_source(app):
    """Press e without saved files shows notification, no crash."""
    with (
        patch("nix_audit.screens.packages.get_installed_packages") as mock_get,
        patch(
            "nix_audit.screens.packages.get_package_sizes",
            new_callable=AsyncMock,
            return_value={},
        ),
    ):
        mock_get.return_value = [
            {"name": "git", "version": "2.43.0", "store_path": "/nix/store/abc-git-2.43.0"},
        ]
        async with app.run_test() as pilot:
            await pilot.pause()
            app.db.upsert_package("git", "2.43.0", "/nix/store/abc-git-2.43.0")
            from nix_audit.screens.detail import DetailScreen

            app.push_screen(DetailScreen("git"))
            await pilot.pause()

            # No saved files, so pressing e should show notification
            with patch(
                "nix_audit.screens.detail.get_saved_sources_dir",
                return_value=None,
            ):
                await pilot.press("e")
                await pilot.pause()
                # Should not crash
