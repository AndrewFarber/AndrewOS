from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.nix import get_installed_packages, get_package_sizes, search_packages


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
async def test_get_installed_packages_gcroot_fallback(mock_subprocess, sample_hm_output, tmp_path):
    """When home-manager packages fails, fall back to gcroot."""
    # home-manager packages fails
    hm_proc = AsyncMock()
    hm_proc.communicate.return_value = (b"", b"")
    hm_proc.returncode = 1

    # nix-store query succeeds
    nix_proc = AsyncMock()
    nix_proc.communicate.return_value = (sample_hm_output.encode(), b"")
    nix_proc.returncode = 0

    mock_subprocess.side_effect = [hm_proc, nix_proc]

    # Set up fake gcroot
    gcroot_dir = tmp_path / "home-manager" / "gcroots"
    gcroot_dir.mkdir(parents=True)
    gen_dir = tmp_path / "generation"
    gen_dir.mkdir()
    home_path = gen_dir / "home-path"
    home_path.mkdir()
    (gcroot_dir / "current-home").symlink_to(gen_dir)

    with patch.dict("os.environ", {"XDG_STATE_HOME": str(tmp_path)}):
        packages = await get_installed_packages()

    assert len(packages) == 3
    assert mock_subprocess.call_count == 2


@pytest.mark.asyncio
async def test_get_installed_packages_gcroot_missing(mock_subprocess, tmp_path):
    """Error when both home-manager and gcroot fail."""
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"")
    proc.returncode = 1
    mock_subprocess.return_value = proc

    with patch.dict("os.environ", {"XDG_STATE_HOME": str(tmp_path)}):
        with pytest.raises(RuntimeError, match="gcroot not found"):
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
    # Verify nixpkgs_attr is preserved
    for r in results:
        assert "nixpkgs_attr" in r
        assert r["nixpkgs_attr"] == r["name"]  # simple case, no nesting


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


@pytest.mark.asyncio
async def test_get_package_sizes(mock_subprocess):
    """nix path-info --json returns sizes keyed by store path."""
    import json

    path_info = {
        "/nix/store/abc-hello-2.12.1": {"narSize": 12345},
        "/nix/store/def-git-2.43.0": {"narSize": 67890},
    }
    proc = AsyncMock()
    proc.communicate.return_value = (json.dumps(path_info).encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    sizes = await get_package_sizes(["/nix/store/abc-hello-2.12.1", "/nix/store/def-git-2.43.0"])
    assert sizes["/nix/store/abc-hello-2.12.1"] == 12345
    assert sizes["/nix/store/def-git-2.43.0"] == 67890


@pytest.mark.asyncio
async def test_get_package_sizes_empty():
    """Empty input returns empty dict without calling nix."""
    sizes = await get_package_sizes([])
    assert sizes == {}


@pytest.mark.asyncio
async def test_get_package_sizes_failure(mock_subprocess):
    """Gracefully returns empty dict on nix path-info failure."""
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"error")
    proc.returncode = 1
    mock_subprocess.return_value = proc

    sizes = await get_package_sizes(["/nix/store/abc-hello-2.12.1"])
    assert sizes == {}
