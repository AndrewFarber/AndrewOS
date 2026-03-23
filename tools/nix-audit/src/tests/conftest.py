import pytest
from pathlib import Path

from nix_audit.models.database import AuditDatabase


@pytest.fixture
def tmp_db(tmp_path):
    """Create a temporary database for testing."""
    db = AuditDatabase(db_path=tmp_path / "test.db")
    yield db
    db.close()


@pytest.fixture
def sample_hm_output():
    """Sample home-manager packages output."""
    return (
        "/nix/store/abc123-hello-2.12.1\n"
        "/nix/store/def456-git-2.43.0\n"
        "/nix/store/ghi789-ripgrep-14.1.0\n"
    )


@pytest.fixture
def sample_nix_search_json():
    """Sample nix search --json output."""
    return '''{
  "legacyPackages.x86_64-linux.hello": {
    "pname": "hello",
    "version": "2.12.1",
    "description": "A program that produces a familiar, friendly greeting"
  },
  "legacyPackages.x86_64-linux.hello-wayland": {
    "pname": "hello-wayland",
    "version": "0.1",
    "description": "Hello world Wayland client"
  }
}'''


@pytest.fixture
def sample_derivation_source():
    """Sample Nix derivation source."""
    return '''\
# default.nix
{ lib, stdenv, fetchurl }:

stdenv.mkDerivation rec {
  pname = "hello";
  version = "2.12.1";

  src = fetchurl {
    url = "mirror://gnu/hello/hello-${version}.tar.gz";
    sha256 = "sha256-jZkUKv2SV28wsM18tCqNxoCZmLnkLAEzWHRnbaN0jY=";
  };

  meta = with lib; {
    description = "A program that produces a familiar, friendly greeting";
    license = licenses.gpl3Plus;
    platforms = platforms.all;
  };
}
'''


@pytest.fixture
def sample_claude_report():
    """Sample Claude audit report."""
    return """\
# Security Audit: hello 2.12.1

## Risk Level: LOW

## 1. Supply Chain Risks
- Source fetched via HTTPS (mirror://gnu redirects to HTTPS mirrors)
- SHA256 hash is pinned
- Official GNU upstream source

## 2. Build-Time Risks
- Standard build dependencies only (stdenv)
- No custom build phases
- No network access during build

## 3. Runtime Risks
- No postInstall hooks
- No elevated permissions
- Minimal runtime dependencies

## 4. NixOS-Specific Risks
- No sandbox bypasses
- No impure environment variables
- Standard derivation pattern

## Summary
This is a minimal, well-packaged GNU utility with no security concerns.
"""


@pytest.fixture
def sample_vulnix_output():
    """Sample vulnix output with CVEs."""
    return """\
hello-2.12.1
  CVE-2021-12345
  CVE-2021-67890
"""


@pytest.fixture
def sample_vulnix_clean():
    """Sample vulnix output with no CVEs."""
    return ""
