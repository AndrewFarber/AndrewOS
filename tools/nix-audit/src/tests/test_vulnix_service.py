from nix_audit.services.vulnix import format_vulnix_report, parse_vulnix_output


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
