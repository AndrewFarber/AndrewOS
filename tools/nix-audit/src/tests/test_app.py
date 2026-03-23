from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path

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
    with patch("nix_audit.screens.packages.get_installed_packages") as mock_get:
        mock_get.return_value = mock_packages
        test_app = NixAuditApp()
        test_app.db = AuditDatabase(db_path=tmp_path / "test.db")
        yield test_app
        test_app.db.close()


@pytest.mark.asyncio
async def test_app_starts(app):
    async with app.run_test() as pilot:
        assert app.title == "nix-audit"


@pytest.mark.asyncio
async def test_packages_screen_loads(app):
    with patch("nix_audit.screens.packages.get_installed_packages") as mock_get:
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
    with patch("nix_audit.screens.packages.get_installed_packages") as mock_get:
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
    with patch("nix_audit.screens.packages.get_installed_packages") as mock_get:
        mock_get.return_value = []
        async with app.run_test() as pilot:
            await pilot.pause()
            await pilot.press("q")
