import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.nix import get_installed_packages, search_packages


@pytest.fixture
def mock_subprocess():
    with patch("nix_audit.services.nix.asyncio.create_subprocess_exec") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_installed_packages(mock_subprocess, sample_hm_output):
    proc = AsyncMock()
    proc.communicate.return_value = (sample_hm_output.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    packages = await get_installed_packages()
    assert len(packages) == 3
    names = [p["name"] for p in packages]
    assert "git" in names
    assert "hello" in names
    assert "ripgrep" in names


@pytest.mark.asyncio
async def test_get_installed_packages_versions(mock_subprocess, sample_hm_output):
    proc = AsyncMock()
    proc.communicate.return_value = (sample_hm_output.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    packages = await get_installed_packages()
    pkg_map = {p["name"]: p for p in packages}
    assert pkg_map["hello"]["version"] == "2.12.1"
    assert pkg_map["git"]["version"] == "2.43.0"


@pytest.mark.asyncio
async def test_get_installed_packages_error(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"command not found")
    proc.returncode = 127
    mock_subprocess.return_value = proc

    with pytest.raises(RuntimeError, match="home-manager packages failed"):
        await get_installed_packages()


@pytest.mark.asyncio
async def test_get_installed_packages_empty(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    packages = await get_installed_packages()
    assert packages == []


@pytest.mark.asyncio
async def test_search_packages(mock_subprocess, sample_nix_search_json):
    proc = AsyncMock()
    proc.communicate.return_value = (sample_nix_search_json.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    results = await search_packages("hello")
    assert len(results) == 2
    names = [r["name"] for r in results]
    assert "hello" in names
    assert "hello-wayland" in names


@pytest.mark.asyncio
async def test_search_packages_error(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"error")
    proc.returncode = 1
    mock_subprocess.return_value = proc

    with pytest.raises(RuntimeError, match="nix search failed"):
        await search_packages("hello")


@pytest.mark.asyncio
async def test_search_packages_empty(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    results = await search_packages("nonexistent")
    assert results == []
