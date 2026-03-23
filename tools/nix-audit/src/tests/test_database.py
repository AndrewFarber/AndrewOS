import pytest


def test_schema_migration(tmp_db):
    """Tables should exist after initialization."""
    tables = tmp_db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    names = [t["name"] for t in tables]
    assert "packages" in names
    assert "audits" in names


def test_upsert_package_insert(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1", "/nix/store/abc-hello-2.12.1")
    pkg = tmp_db.get_package("hello")
    assert pkg is not None
    assert pkg["name"] == "hello"
    assert pkg["version"] == "2.12.1"
    assert pkg["store_path"] == "/nix/store/abc-hello-2.12.1"


def test_upsert_package_update(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1", "/nix/store/abc-hello-2.12.1")
    tmp_db.upsert_package("hello", "2.13.0", "/nix/store/xyz-hello-2.13.0")
    pkg = tmp_db.get_package("hello")
    assert pkg["version"] == "2.13.0"
    assert pkg["store_path"] == "/nix/store/xyz-hello-2.13.0"


def test_get_all_packages(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    tmp_db.upsert_package("git", "2.43.0")
    pkgs = tmp_db.get_all_packages()
    assert len(pkgs) == 2
    assert pkgs[0]["name"] == "git"
    assert pkgs[1]["name"] == "hello"


def test_audit_status_none(tmp_db):
    assert tmp_db.get_audit_status("hello") == "none"


def test_audit_status_none_with_package(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    assert tmp_db.get_audit_status("hello") == "none"


def test_audit_status_current(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    tmp_db.save_audit("hello", "2.12.1", "report", "summary")
    assert tmp_db.get_audit_status("hello") == "current"


def test_audit_status_outdated(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    tmp_db.save_audit("hello", "2.11.0", "old report", "old summary")
    assert tmp_db.get_audit_status("hello") == "outdated"


def test_save_audit_missing_package(tmp_db):
    with pytest.raises(ValueError, match="not found"):
        tmp_db.save_audit("nonexistent", "1.0", "report", "summary")


def test_get_audits_for_package(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    tmp_db.save_audit("hello", "2.12.1", "report1", "summary1", "claude")
    tmp_db.save_audit("hello", "2.12.1", "report2", "summary2", "vulnix")
    audits = tmp_db.get_audits_for_package("hello")
    assert len(audits) == 2
    types = {a["audit_type"] for a in audits}
    assert types == {"claude", "vulnix"}


def test_get_audits_empty(tmp_db):
    assert tmp_db.get_audits_for_package("nonexistent") == []


def test_upsert_packages_batch(tmp_db):
    packages = [
        {"name": "hello", "version": "2.12.1", "store_path": "/nix/store/abc-hello-2.12.1"},
        {"name": "git", "version": "2.43.0", "store_path": "/nix/store/def-git-2.43.0"},
        {"name": "ripgrep", "version": "14.1.0", "store_path": "/nix/store/ghi-ripgrep-14.1.0"},
    ]
    tmp_db.upsert_packages_batch(packages)
    all_pkgs = tmp_db.get_all_packages()
    assert len(all_pkgs) == 3
    names = {p["name"] for p in all_pkgs}
    assert names == {"hello", "git", "ripgrep"}


def test_upsert_packages_batch_updates_existing(tmp_db):
    tmp_db.upsert_package("hello", "2.12.0", "/nix/store/old-hello-2.12.0")
    packages = [
        {"name": "hello", "version": "2.12.1", "store_path": "/nix/store/new-hello-2.12.1"},
    ]
    tmp_db.upsert_packages_batch(packages)
    pkg = tmp_db.get_package("hello")
    assert pkg["version"] == "2.12.1"


def test_get_all_audit_info(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    tmp_db.upsert_package("git", "2.43.0")
    tmp_db.save_audit("hello", "2.12.1", "report", "summary")

    info = tmp_db.get_all_audit_info()
    assert info["hello"]["status"] == "current"
    assert info["hello"]["last_audited"] != "never"
    assert info["git"]["status"] == "none"
    assert info["git"]["last_audited"] == "never"


def test_get_all_audit_info_outdated(tmp_db):
    tmp_db.upsert_package("hello", "2.13.0")
    tmp_db.save_audit("hello", "2.12.1", "old report", "old summary")

    info = tmp_db.get_all_audit_info()
    assert info["hello"]["status"] == "outdated"
