from unittest.mock import AsyncMock, patch

import pytest

from nix_audit.services.vulnix import format_vulnix_report, parse_vulnix_output, scan_package


def test_parse_vulnix_output(sample_vulnix_output):
    cves = parse_vulnix_output(sample_vulnix_output)
    assert len(cves) == 2
    assert cves[0]["cve_id"] == "CVE-2021-12345"
    assert cves[1]["cve_id"] == "CVE-2021-67890"
    assert cves[0]["package"] == "hello-2.12.1"


def test_parse_vulnix_output_clean(sample_vulnix_clean):
    cves = parse_vulnix_output(sample_vulnix_clean)
    assert cves == []


def test_format_vulnix_report_with_cves():
    cves = [
        {"cve_id": "CVE-2021-12345", "package": "hello-2.12.1"},
        {"cve_id": "CVE-2021-67890", "package": "hello-2.12.1"},
    ]
    report = format_vulnix_report(cves, "hello", "2.12.1")
    assert "hello" in report
    assert "CVE-2021-12345" in report
    assert "CVE-2021-67890" in report
    assert "2" in report  # count


def test_format_vulnix_report_clean():
    report = format_vulnix_report([], "hello", "2.12.1")
    assert "No known CVEs" in report


@pytest.mark.asyncio
async def test_scan_package_real_error():
    """Vulnix failures with no stdout should raise RuntimeError."""
    with patch("nix_audit.services.vulnix.asyncio.create_subprocess_exec") as mock:
        proc = AsyncMock()
        proc.communicate.return_value = (b"", b"vulnix: command not found")
        proc.returncode = 127
        mock.return_value = proc

        with pytest.raises(RuntimeError, match="vulnix failed"):
            await scan_package("/nix/store/abc-hello-2.12.1")


@pytest.mark.asyncio
async def test_scan_package_cves_found():
    """Non-zero exit with stdout (CVEs found) should not raise."""
    with patch("nix_audit.services.vulnix.asyncio.create_subprocess_exec") as mock:
        proc = AsyncMock()
        proc.communicate.return_value = (
            b"hello-2.12.1\n  CVE-2021-12345\n",
            b"",
        )
        proc.returncode = 2
        mock.return_value = proc

        cves = await scan_package("/nix/store/abc-hello-2.12.1")
        assert len(cves) == 1
        assert cves[0]["cve_id"] == "CVE-2021-12345"
