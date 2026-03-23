import asyncio
import logging
import shutil
from pathlib import Path

log = logging.getLogger(__name__)

MAX_SOURCE_BYTES = 100_000  # 100KB cap to avoid huge prompts
SOURCES_DIR = Path.home() / ".local" / "share" / "nix-audit" / "sources"


async def _resolve_nix_files(package_name: str) -> list[Path] | None:
    """Run nix eval meta.position and return list of .nix file paths."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "nix",
            "eval",
            f"nixpkgs#{package_name}.meta.position",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError:
        log.error("nix not found in PATH")
        return None
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

    # Collect the main file first, then siblings
    files = [path]
    total_size = path.stat().st_size
    for sibling in sorted(path.parent.glob("*.nix")):
        if sibling != path and sibling.is_file():
            size = sibling.stat().st_size
            if total_size + size > MAX_SOURCE_BYTES:
                break
            total_size += size
            files.append(sibling)

    return files


def _read_source(files: list[Path]) -> str | None:
    """Read .nix file contents and concatenate them."""
    sources = []
    total_size = 0
    for f in files:
        try:
            content = f.read_text()
            total_size += len(content)
            sources.append(f"# {f.name}\n{content}")
        except OSError:
            if not sources:
                log.error("Failed to read derivation file %s", f)
                return None
            continue

    log.info("Read derivation source (%d bytes, %d files)", total_size, len(sources))
    return "\n\n".join(sources) if sources else None


def _copy_files(files: list[Path], package_name: str) -> list[Path] | None:
    """Copy .nix files to the sources directory."""
    dest_dir = SOURCES_DIR / package_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for f in files:
        try:
            dest = dest_dir / f.name
            shutil.copy2(f, dest)
            saved.append(dest)
        except OSError:
            log.error("Failed to copy %s to %s", f, dest_dir)
            continue

    if not saved:
        return None

    log.info("Saved %d source file(s) for %s to %s", len(saved), package_name, dest_dir)
    return saved


async def get_derivation_source(package_name: str) -> str | None:
    """Fetch the Nix derivation source for a package using meta.position."""
    files = await _resolve_nix_files(package_name)
    if not files:
        return None
    return _read_source(files)


async def save_derivation_files(package_name: str) -> list[Path] | None:
    """Copy derivation .nix files to ~/.local/share/nix-audit/sources/<package>/."""
    files = await _resolve_nix_files(package_name)
    if not files:
        return None
    return _copy_files(files, package_name)


async def resolve_and_read_source(package_name: str) -> tuple[str | None, list[Path] | None]:
    """Resolve nix files once, return (source_text, saved_file_paths).

    Avoids calling nix eval twice when both source and saved files are needed.
    """
    files = await _resolve_nix_files(package_name)
    if not files:
        return None, None
    source = _read_source(files)
    saved = _copy_files(files, package_name)
    return source, saved


def get_saved_sources_dir(package_name: str) -> Path | None:
    """Check if saved source files exist for a package. Returns dir path or None."""
    dest_dir = SOURCES_DIR / package_name
    if dest_dir.is_dir() and any(dest_dir.iterdir()):
        return dest_dir
    return None
