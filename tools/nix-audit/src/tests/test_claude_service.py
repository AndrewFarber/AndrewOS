import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.claude import (
    AUDIT_PROMPT,
    _safe_filename,
    parse_claude_response,
    render_report_markdown,
    run_claude_audit,
)


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

    result = await run_claude_audit("hello", "2.12.1", "source code")
    assert result["risk_level"] == "LOW"
    assert len(result["findings"]) == 1
    assert "report_markdown" in result
    assert "Security Audit" in result["report_markdown"]

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


@pytest.mark.asyncio
async def test_run_claude_audit_timeout(mock_subprocess):
    proc = AsyncMock()

    async def slow_communicate():
        await asyncio.sleep(10)
        return (b"", b"")

    proc.communicate = slow_communicate
    proc.kill = lambda: None
    proc.wait = AsyncMock()
    mock_subprocess.return_value = proc

    with patch("nix_audit.services.claude.AUDIT_TIMEOUT", 0.01):
        with pytest.raises(RuntimeError, match="timed out"):
            await run_claude_audit("hello", "2.12.1", "source code")


@pytest.mark.asyncio
async def test_run_claude_audit_invalid_json_fallback(mock_subprocess):
    proc = AsyncMock()
    proc.communicate.return_value = (b"this is not json", b"")
    proc.returncode = 0
    mock_subprocess.return_value = proc

    result = await run_claude_audit("hello", "2.12.1", "source code")
    assert result["risk_level"] == "UNKNOWN"
    assert result["findings"] == []
    assert "raw_response" in result
    assert "JSON parsing failed" in result["report_markdown"]


def test_parse_claude_response_valid():
    raw = json.dumps(
        {
            "risk_level": "HIGH",
            "findings": [
                {
                    "category": "supply_chain",
                    "severity": "high",
                    "title": "No hash pinning",
                    "detail": "fetchurl has no sha256",
                    "recommendation": "Add sha256 hash",
                }
            ],
            "summary": "Missing hash pinning is a serious concern.",
        }
    )
    data = parse_claude_response(raw)
    assert data["risk_level"] == "HIGH"
    assert len(data["findings"]) == 1
    assert data["findings"][0]["severity"] == "high"
    assert data["summary"] == "Missing hash pinning is a serious concern."


def test_parse_claude_response_strips_fences():
    inner = json.dumps({"risk_level": "LOW", "findings": [], "summary": "OK."})
    raw = f"```json\n{inner}\n```"
    data = parse_claude_response(raw)
    assert data["risk_level"] == "LOW"


def test_parse_claude_response_normalizes_risk():
    raw = json.dumps({"risk_level": "bogus", "findings": [], "summary": "x"})
    data = parse_claude_response(raw)
    assert data["risk_level"] == "UNKNOWN"


def test_parse_claude_response_validates_findings():
    raw = json.dumps(
        {
            "risk_level": "LOW",
            "findings": [
                {"category": "runtime", "severity": "low", "title": "Minor"},
                "not a dict",
                42,
            ],
            "summary": "x",
        }
    )
    data = parse_claude_response(raw)
    assert len(data["findings"]) == 1
    assert data["findings"][0]["title"] == "Minor"


def test_render_report_markdown():
    data = {
        "risk_level": "MEDIUM",
        "findings": [
            {
                "category": "supply_chain",
                "severity": "medium",
                "title": "Third-party mirror",
                "detail": "Source fetched from non-official mirror.",
                "recommendation": "Use official upstream URL.",
            },
            {
                "category": "runtime",
                "severity": "low",
                "title": "Large runtime closure",
                "detail": "Many runtime dependencies.",
                "recommendation": None,
            },
        ],
        "summary": "Some supply chain concerns.",
    }
    md = render_report_markdown(data, "example", "1.0")
    assert "# Security Audit: example 1.0" in md
    assert "## Risk Level: MEDIUM" in md
    assert "**[MEDIUM]** Third-party mirror" in md
    assert "*Recommendation:* Use official upstream URL." in md
    assert "**[LOW]** Large runtime closure" in md
    assert "## Build-Time Risks" in md
    assert "Some supply chain concerns." in md


def test_render_report_markdown_raw_fallback():
    data = {
        "risk_level": "UNKNOWN",
        "findings": [],
        "summary": "Could not parse.",
        "raw_response": "some raw text from claude",
    }
    md = render_report_markdown(data, "pkg", "1.0")
    assert "JSON parsing failed" in md
    assert "some raw text from claude" in md


def test_prompt_contains_injection_defense():
    assert "UNTRUSTED INPUT" in AUDIT_PROMPT
    assert "<derivation>" in AUDIT_PROMPT
    assert "</derivation>" in AUDIT_PROMPT


def test_prompt_requests_json():
    assert "JSON" in AUDIT_PROMPT
    assert "risk_level" in AUDIT_PROMPT
    assert "findings" in AUDIT_PROMPT


def test_prompt_contains_categories():
    """Verify the prompt includes all 4 security categories."""
    assert "Supply Chain Risks" in AUDIT_PROMPT
    assert "Build-Time Risks" in AUDIT_PROMPT
    assert "Runtime Risks" in AUDIT_PROMPT
    assert "NixOS-Specific Risks" in AUDIT_PROMPT


def test_prompt_contains_key_checks():
    """Verify the prompt includes key security checks."""
    assert "sha256" in AUDIT_PROMPT
    assert "__noChroot" in AUDIT_PROMPT
    assert "builtins.fetchurl" in AUDIT_PROMPT
    assert "impureEnvVars" in AUDIT_PROMPT
    assert "setuid" in AUDIT_PROMPT.lower() or "Setuid" in AUDIT_PROMPT


def test_safe_filename_normal():
    assert _safe_filename("hello", "2.12.1") == "hello-2.12.1.md"


def test_safe_filename_path_traversal():
    result = _safe_filename("../../../etc/passwd", "1.0")
    assert "/" not in result
    assert result.endswith(".md")


def test_safe_filename_special_chars():
    result = _safe_filename("foo bar/baz", "1.0+git")
    assert " " not in result
    assert "/" not in result
    assert "+" not in result
