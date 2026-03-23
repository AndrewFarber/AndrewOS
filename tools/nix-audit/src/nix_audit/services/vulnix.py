import asyncio
import re


async def scan_package(store_path: str) -> list[dict]:
    """Run vulnix on a store path and parse CVE results."""
    proc = await asyncio.create_subprocess_exec(
        "vulnix", store_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    output = stdout.decode()
    # vulnix exits non-zero when CVEs are found, so don't check returncode
    return parse_vulnix_output(output)


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
        f"\nCheck https://nvd.nist.gov/ for details on each CVE."
    )
    return "\n".join(lines)
