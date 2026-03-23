import asyncio
from pathlib import Path


async def get_derivation_source(package_name: str) -> str | None:
    """Fetch the Nix derivation source for a package using meta.position."""
    proc = await asyncio.create_subprocess_exec(
        "nix", "eval", f"nixpkgs#{package_name}.meta.position",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
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
    try:
        sources.append(f"# {path.name}\n{path.read_text()}")
    except OSError:
        return None
    # Also read other .nix files in the same directory
    for sibling in sorted(path.parent.glob("*.nix")):
        if sibling != path and sibling.is_file():
            try:
                sources.append(f"# {sibling.name}\n{sibling.read_text()}")
            except OSError:
                continue
    return "\n\n".join(sources) if sources else None
