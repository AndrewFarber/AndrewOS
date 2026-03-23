import asyncio
from pathlib import Path

AUDIT_PROMPT = """\
You are a Nix package security auditor. Analyze the following Nix derivation source code for package "{name}" version {version}.

Review across these four categories:

## 1. Supply Chain Risks
- Are fetch URLs using HTTPS? Are hashes (sha256) pinned?
- Are sources from official upstreams or third-party mirrors?
- Are patches applied? What do they modify?
- Is the source from a release tarball or a git commit?

## 2. Build-Time Risks
- Unusual build dependencies or native build inputs?
- Custom build phases (preBuild, postBuild, preConfigure) with suspicious commands?
- Network access attempts during build (should be sandboxed)?
- Build scripts that execute arbitrary code from the internet?

## 3. Runtime Risks
- postInstall hooks that modify the system?
- Setuid/setgid bits, capabilities, or elevated permissions?
- Systemd services or wrappers that run as root?
- Runtime dependencies that seem excessive or unexpected?

## 4. NixOS-Specific Risks
- allowedRequisites / allowedReferences bypasses?
- Use of builtins.fetchurl (no hash enforcement)?
- __noChroot = true disabling the sandbox?
- impureEnvVars leaking host environment?
- Overlays or overrides that weaken security defaults?

Produce a structured Markdown report with:
- A risk level header: LOW / MEDIUM / HIGH / CRITICAL
- A findings section for each of the 4 categories
- A summary of key concerns
- Recommendations if applicable

Here is the derivation source:

```nix
{source}
```
"""

REPORT_DIR = Path("/tmp/nix-audit")


async def run_claude_audit(
    name: str, version: str, derivation_source: str
) -> str:
    """Run Claude CLI to produce a security audit report."""
    prompt = AUDIT_PROMPT.format(
        name=name, version=version, source=derivation_source
    )
    proc = await asyncio.create_subprocess_exec(
        "claude", "-p", prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude audit failed (exit {proc.returncode}): {stderr.decode()}"
        )
    report = stdout.decode()
    # Save to /tmp/nix-audit/
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{name}-{version}.md"
    report_path.write_text(report)
    return report
