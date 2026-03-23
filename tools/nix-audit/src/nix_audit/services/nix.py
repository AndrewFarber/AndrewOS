import asyncio
import json
import logging
import os
import re
from pathlib import Path

log = logging.getLogger(__name__)


def _parse_store_paths(lines: list[str]) -> list[dict]:
    """Parse /nix/store/... paths into package dicts."""
    packages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Format: /nix/store/<hash>-<name>-<version>
        match = re.match(r"(/nix/store/[a-z0-9]+-(.+?)-([\d][\d.]*\w*))$", line)
        if match:
            packages.append(
                {
                    "store_path": match.group(1),
                    "name": match.group(2),
                    "version": match.group(3),
                }
            )
        else:
            # Fallback: try splitting on last dash before version-like string
            match = re.match(r"(/nix/store/[a-z0-9]+-(.+))$", line)
            if match:
                full_name = match.group(2)
                ver_match = re.match(r"^(.+?)-([\d][\d.]*.*)$", full_name)
                if ver_match:
                    packages.append(
                        {
                            "store_path": match.group(1),
                            "name": ver_match.group(1),
                            "version": ver_match.group(2),
                        }
                    )
                else:
                    packages.append(
                        {
                            "store_path": match.group(1),
                            "name": full_name,
                            "version": "unknown",
                        }
                    )
    return packages


async def _get_packages_via_gcroot() -> list[str]:
    """Get package store paths from the home-manager gcroot.

    Works when home-manager is used as a NixOS module (where
    ``home-manager packages`` cannot find the nix profile entry).
    """
    state_dir = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state")))
    gcroot = state_dir / "home-manager" / "gcroots" / "current-home"
    if not gcroot.exists():
        raise RuntimeError(f"home-manager gcroot not found at {gcroot}")
    generation = gcroot.resolve()
    home_path = generation / "home-path"
    if not home_path.exists():
        raise RuntimeError(f"home-path not found in {generation}")
    home_path = home_path.resolve()
    proc = await asyncio.create_subprocess_exec(
        "nix-store",
        "-q",
        "--references",
        str(home_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"nix-store query failed: {stderr.decode()}")
    return stdout.decode().strip().splitlines()


async def get_installed_packages() -> list[dict]:
    """Get installed Home Manager packages.

    Tries ``home-manager packages`` first, then falls back to reading the
    home-manager gcroot directly (needed when home-manager runs as a NixOS
    module).
    """
    use_fallback = False
    lines: list[str] = []
    try:
        proc = await asyncio.create_subprocess_exec(
            "home-manager",
            "packages",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            lines = stdout.decode().strip().splitlines()
        else:
            log.warning(
                "home-manager packages returned exit %d, trying gcroot fallback",
                proc.returncode,
            )
            use_fallback = True
    except FileNotFoundError:
        log.warning("home-manager not found in PATH, trying gcroot fallback")
        use_fallback = True

    if use_fallback:
        lines = await _get_packages_via_gcroot()

    packages = [
        p
        for p in _parse_store_paths(lines)
        if not p["name"].startswith("andrewos-")
        and p["version"] != "unknown"
        and not p["version"].endswith("-man")
        and not p["version"].endswith("-terminfo")
    ]
    log.info("Loaded %d installed packages", len(packages))
    return sorted(packages, key=lambda p: p["name"])


async def search_packages(query: str) -> list[dict]:
    """Search nixpkgs via `nix search`."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "nix",
            "search",
            "nixpkgs",
            query,
            "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError:
        msg = "nix not found in PATH"
        log.error(msg)
        raise RuntimeError(msg)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        msg = f"nix search failed (exit {proc.returncode}): {stderr.decode()}"
        log.error(msg)
        raise RuntimeError(msg)
    text = stdout.decode().strip()
    if not text:
        return []
    data = json.loads(text)
    results = []
    for attr_path, info in data.items():
        # attr_path like "legacyPackages.x86_64-linux.hello"
        name = attr_path.split(".")[-1]
        results.append(
            {
                "name": name,
                "version": info.get("version", "unknown"),
                "description": info.get("description", ""),
            }
        )
    return sorted(results, key=lambda p: p["name"])
