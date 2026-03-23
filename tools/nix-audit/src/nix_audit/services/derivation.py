import asyncio
import logging
from pathlib import Path

log = logging.getLogger(__name__)

MAX_SOURCE_BYTES = 100_000  # 100KB cap to avoid huge prompts


async def get_derivation_source(package_name: str) -> str | None:
    """Fetch the Nix derivation source for a package using meta.position."""
    proc = await asyncio.create_subprocess_exec(
        "nix", "eval", f"nixpkgs#{package_name}.meta.position",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        err = stderr.decode().strip()
        log.warning("nix eval meta.position failed for %s: %s", package_name, err)
        return None
    position = stdout.decode().strip().strip('"')
    if not position:
        return None
    # position is like "/nix/store/...-source/pkgs/foo/default.nix:42"
    file_path = position.split(":")[0]
    path = Path(file_path)
    if not path.exists():
        return None
    # Read the main file and any related files in the same directory
    sources = []
    total_size = 0
    try:
        content = path.read_text()
        total_size += len(content)
        sources.append(f"# {path.name}\n{content}")
    except OSError:
        log.error("Failed to read derivation file %s", path)
        return None
    # Also read other .nix files in the same directory (up to size cap)
    for sibling in sorted(path.parent.glob("*.nix")):
        if sibling != path and sibling.is_file():
            try:
                content = sibling.read_text()
                if total_size + len(content) > MAX_SOURCE_BYTES:
                    break
                total_size += len(content)
                sources.append(f"# {sibling.name}\n{content}")
            except OSError:
                continue
    log.info("Fetched derivation source for %s (%d bytes)", package_name, total_size)
    return "\n\n".join(sources) if sources else None
