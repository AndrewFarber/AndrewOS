from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.derivation import MAX_SOURCE_BYTES, get_derivation_source


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
