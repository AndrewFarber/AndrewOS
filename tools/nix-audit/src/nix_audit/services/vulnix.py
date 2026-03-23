import asyncio
import logging
import re

log = logging.getLogger(__name__)


async def scan_package(store_path: str) -> list[dict]:
    """Run vulnix on a store path and parse CVE results."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "vulnix", store_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError:
        msg = "vulnix not found in PATH"
        log.error(msg)
        raise RuntimeError(msg)
    stdout, stderr = await proc.communicate()
    output = stdout.decode()
    err = stderr.decode().strip()
    # vulnix exits 2 when CVEs are found — that's expected.
    # Any other non-zero exit with no stdout is a real error.
    if proc.returncode != 0 and not output.strip():
        msg = f"vulnix failed (exit {proc.returncode}): {err}"
        log.error(msg)
        raise RuntimeError(msg)
    cves = parse_vulnix_output(output)
    log.info("vulnix scan of %s found %d CVE(s)", store_path, len(cves))
    return cves


def parse_vulnix_output(output: str) -> list[dict]:
    """Parse vulnix output into a list of CVE dicts."""
    cves = []
    current_pkg = None
    for line in output.splitlines():
        line = line.rstrip()
        if not line:
            continue
        # Package header line
        if not line.startswith(" ") and not line.startswith("CVE"):
            current_pkg = line.strip()
            continue
        # CVE line
        cve_match = re.match(r"\s*(CVE-\d{4}-\d+)", line)
        if cve_match:
            cves.append({
                "cve_id": cve_match.group(1),
                "package": current_pkg,
            })
    return cves


def format_vulnix_report(cves: list[dict], package_name: str, version: str) -> str:
    """Format CVE results as a Markdown report."""
    if not cves:
        return (
            f"# Vulnix CVE Scan: {package_name} {version}\n\n"
            f"No known CVEs found for this package.\n"
        )
    lines = [
        f"# Vulnix CVE Scan: {package_name} {version}\n",
        f"Found **{len(cves)}** known CVE(s):\n",
    ]
    for cve in cves:
        lines.append(f"- **{cve['cve_id']}**")
    lines.append(
        "\nCheck https://nvd.nist.gov/ for details on each CVE."
    )
    return "\n".join(lines)
