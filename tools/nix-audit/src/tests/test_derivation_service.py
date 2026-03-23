from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.derivation import (
    MAX_SOURCE_BYTES,
    get_derivation_source,
    get_saved_sources_dir,
    save_derivation_files,
)


@pytest.fixture
def mock_subprocess():
    with patch("nix_audit.services.derivation.asyncio.create_subprocess_exec") as mock:
        yield mock


@pytest.mark.asyncio
async def test_get_derivation_source(mock_subprocess, tmp_path):
    # Create a fake nix file
    nix_file = tmp_path / "default.nix"
    nix_file.write_text('{ pname = "hello"; }')
    position = f'"{nix_file}:1"'

    proc = AsyncMock()
    proc.communicate.return_value = (position.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    source = await get_derivation_source("hello")
    assert source is not None
    assert 'pname = "hello"' in source


@pytest.mark.asyncio
async def test_get_derivation_source_with_siblings(mock_subprocess, tmp_path):
    main_file = tmp_path / "default.nix"
    main_file.write_text("main content")
    sibling = tmp_path / "common.nix"
    sibling.write_text("common content")

    position = f'"{main_file}:1"'
    proc = AsyncMock()
    proc.communicate.return_value = (position.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    source = await get_derivation_source("hello")
    assert "main content" in source
    assert "common content" in source


@pytest.mark.asyncio
async def test_get_derivation_source_nix_eval_fails(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"error")
    proc.returncode = 1
    mock_subprocess.return_value = proc

    source = await get_derivation_source("nonexistent")
    assert source is None


@pytest.mark.asyncio
async def test_get_derivation_source_missing_file(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b'"/nonexistent/path.nix:1"', b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    source = await get_derivation_source("hello")
    assert source is None


@pytest.mark.asyncio
async def test_get_derivation_source_size_cap(mock_subprocess, tmp_path):
    """Siblings exceeding MAX_SOURCE_BYTES are excluded."""
    main_file = tmp_path / "default.nix"
    main_file.write_text("main content")

    # Create a sibling that would push over the limit
    big_sibling = tmp_path / "big.nix"
    big_sibling.write_text("x" * (MAX_SOURCE_BYTES + 1))

    position = f'"{main_file}:1"'
    proc = AsyncMock()
    proc.communicate.return_value = (position.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    source = await get_derivation_source("hello")
    assert "main content" in source
    assert "x" * 100 not in source


@pytest.mark.asyncio
async def test_save_derivation_files(mock_subprocess, tmp_path):
    """save_derivation_files copies .nix files to SOURCES_DIR."""
    nix_file = tmp_path / "default.nix"
    nix_file.write_text('{ pname = "hello"; }')
    sibling = tmp_path / "common.nix"
    sibling.write_text("common stuff")

    position = f'"{nix_file}:1"'
    proc = AsyncMock()
    proc.communicate.return_value = (position.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    dest_dir = tmp_path / "sources"
    with patch("nix_audit.services.derivation.SOURCES_DIR", dest_dir):
        saved = await save_derivation_files("hello")

    assert saved is not None
    assert len(saved) == 2
    names = {p.name for p in saved}
    assert "default.nix" in names
    assert "common.nix" in names
    # Verify content was copied
    for p in saved:
        assert p.exists()
        assert p.read_text() != ""


@pytest.mark.asyncio
async def test_save_derivation_files_not_found(mock_subprocess):
    """save_derivation_files returns None when nix eval fails."""
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"error")
    proc.returncode = 1
    mock_subprocess.return_value = proc

    saved = await save_derivation_files("nonexistent")
    assert saved is None


def test_get_saved_sources_dir_exists(tmp_path):
    """get_saved_sources_dir returns path when files exist."""
    pkg_dir = tmp_path / "hello"
    pkg_dir.mkdir()
    (pkg_dir / "default.nix").write_text("content")

    with patch("nix_audit.services.derivation.SOURCES_DIR", tmp_path):
        result = get_saved_sources_dir("hello")

    assert result is not None
    assert result == pkg_dir


def test_get_saved_sources_dir_missing(tmp_path):
    """get_saved_sources_dir returns None when no files saved."""
    with patch("nix_audit.services.derivation.SOURCES_DIR", tmp_path):
        result = get_saved_sources_dir("nonexistent")

    assert result is None


def test_get_saved_sources_dir_empty(tmp_path):
    """get_saved_sources_dir returns None when dir exists but is empty."""
    pkg_dir = tmp_path / "hello"
    pkg_dir.mkdir()

    with patch("nix_audit.services.derivation.SOURCES_DIR", tmp_path):
        result = get_saved_sources_dir("hello")

    assert result is None
