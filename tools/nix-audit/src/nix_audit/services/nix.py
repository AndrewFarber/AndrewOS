import asyncio
import json
import re


async def get_installed_packages() -> list[dict]:
    """Get installed Home Manager packages via `home-manager packages`."""
    proc = await asyncio.create_subprocess_exec(
        "home-manager", "packages",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"home-manager packages failed (exit {proc.returncode}): {stderr.decode()}"
        )
    packages = []
    for line in stdout.decode().strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Format: /nix/store/<hash>-<name>-<version>
        # Extract name and version from store path
        match = re.match(r"(/nix/store/[a-z0-9]+-(.+?)-([\d][\d.]*\w*))$", line)
        if match:
            packages.append({
                "store_path": match.group(1),
                "name": match.group(2),
                "version": match.group(3),
            })
        else:
            # Fallback: try splitting on last dash before version-like string
            match = re.match(r"(/nix/store/[a-z0-9]+-(.+))$", line)
            if match:
                full_name = match.group(2)
                # Try to split name-version
                ver_match = re.match(r"^(.+?)-([\d][\d.]*.*)$", full_name)
                if ver_match:
                    packages.append({
                        "store_path": match.group(1),
                        "name": ver_match.group(1),
                        "version": ver_match.group(2),
                    })
                else:
                    packages.append({
                        "store_path": match.group(1),
                        "name": full_name,
                        "version": "unknown",
                    })
    return sorted(packages, key=lambda p: p["name"])


async def search_packages(query: str) -> list[dict]:
    """Search nixpkgs via `nix search`."""
    proc = await asyncio.create_subprocess_exec(
        "nix", "search", "nixpkgs", query, "--json",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"nix search failed (exit {proc.returncode}): {stderr.decode()}"
        )
    text = stdout.decode().strip()
    if not text:
        return []
    data = json.loads(text)
    results = []
    for attr_path, info in data.items():
        # attr_path like "legacyPackages.x86_64-linux.hello"
        name = attr_path.split(".")[-1]
        results.append({
            "name": name,
            "version": info.get("version", "unknown"),
            "description": info.get("description", ""),
        })
    return sorted(results, key=lambda p: p["name"])
