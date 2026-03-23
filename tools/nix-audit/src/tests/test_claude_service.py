from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.claude import AUDIT_PROMPT, _safe_filename, run_claude_audit


@pytest.fixture
def mock_subprocess():
    with patch("nix_audit.services.claude.asyncio.create_subprocess_exec") as mock:
        yield mock


@pytest.mark.asyncio
async def test_run_claude_audit(mock_subprocess, sample_claude_report):
    proc = AsyncMock()
    proc.communicate.return_value = (sample_claude_report.encode(), b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    report = await run_claude_audit("hello", "2.12.1", "source code")
    assert "Security Audit" in report
    assert "Risk Level" in report

    # Verify claude was called with -p flag
    call_args = mock_subprocess.call_args[0]
    assert call_args[0] == "claude"
    assert call_args[1] == "-p"


@pytest.mark.asyncio
async def test_run_claude_audit_error(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"", b"claude not found")
    proc.returncode = 127
    mock_subprocess.return_value = proc

    with pytest.raises(RuntimeError, match="claude audit failed"):
        await run_claude_audit("hello", "2.12.1", "source code")


def test_prompt_contains_categories():
    """Verify the prompt includes all 4 security categories."""
    prompt = AUDIT_PROMPT
    assert "Supply Chain Risks" in prompt
    assert "Build-Time Risks" in prompt
    assert "Runtime Risks" in prompt
    assert "NixOS-Specific Risks" in prompt


def test_prompt_contains_key_checks():
    """Verify the prompt includes key security checks."""
    prompt = AUDIT_PROMPT
    assert "sha256" in prompt
    assert "__noChroot" in prompt
    assert "builtins.fetchurl" in prompt
    assert "impureEnvVars" in prompt
    assert "setuid" in prompt.lower() or "Setuid" in prompt


def test_safe_filename_normal():
    assert _safe_filename("hello", "2.12.1") == "hello-2.12.1.md"


def test_safe_filename_path_traversal():
    result = _safe_filename("../../../etc/passwd", "1.0")
    assert "/" not in result
    # Path separators are stripped, so traversal is impossible
    assert result.endswith(".md")


def test_safe_filename_special_chars():
    result = _safe_filename("foo bar/baz", "1.0+git")
    assert " " not in result
    assert "/" not in result
    assert "+" not in result
