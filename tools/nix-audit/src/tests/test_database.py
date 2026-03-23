import pytest


def test_schema_migration(tmp_db):
    """Tables should exist after initialization."""
    tables = tmp_db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    names = [t["name"] for t in tables]
    assert "packages" in names
    assert "audits" in names
    assert "findings" in names


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


def test_save_and_get_findings(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    audit_id = tmp_db.save_audit("hello", "2.12.1", "report", "summary", "claude")
    findings = [
        {
            "category": "supply_chain",
            "severity": "high",
            "title": "No hash pinning",
            "detail": "fetchurl missing sha256",
            "recommendation": "Add sha256 hash",
        },
        {
            "category": "runtime",
            "severity": "low",
            "title": "Large closure",
            "detail": "Many runtime deps",
            "recommendation": None,
        },
    ]
    tmp_db.save_findings(audit_id, findings)
    saved = tmp_db.get_findings_for_audit(audit_id)
    assert len(saved) == 2
    assert saved[0]["category"] == "supply_chain"
    assert saved[0]["severity"] == "high"
    assert saved[1]["recommendation"] is None


def test_get_findings_empty(tmp_db):
    tmp_db.upsert_package("hello", "2.12.1")
    audit_id = tmp_db.save_audit("hello", "2.12.1", "report", "summary")
    assert tmp_db.get_findings_for_audit(audit_id) == []


def test_upsert_package_preserves_store_path(tmp_db):
    """Upserting without store_path should not wipe an existing one."""
    tmp_db.upsert_package("hello", "2.12.1", "/nix/store/abc-hello-2.12.1")
    tmp_db.upsert_package("hello", "unknown")
    pkg = tmp_db.get_package("hello")
    assert pkg["store_path"] == "/nix/store/abc-hello-2.12.1"


def test_upsert_packages_batch_preserves_store_path(tmp_db):
    """Batch upserting without store_path should not wipe an existing one."""
    tmp_db.upsert_package("hello", "2.12.1", "/nix/store/abc-hello-2.12.1")
    tmp_db.upsert_packages_batch([{"name": "hello", "version": "2.13.0", "store_path": None}])
    pkg = tmp_db.get_package("hello")
    assert pkg["version"] == "2.13.0"
    assert pkg["store_path"] == "/nix/store/abc-hello-2.12.1"


def test_save_audit_returns_id(tmp_db):
    """save_audit should return the new audit's id."""
    tmp_db.upsert_package("hello", "2.12.1")
    audit_id = tmp_db.save_audit("hello", "2.12.1", "report", "summary")
    assert isinstance(audit_id, int)
    assert audit_id > 0


def test_save_findings_with_audit_id(tmp_db):
    """save_findings links findings to the correct audit via explicit id."""
    tmp_db.upsert_package("hello", "2.12.1")
    audit_id_1 = tmp_db.save_audit("hello", "2.12.1", "report1", "summary1", "claude")
    audit_id_2 = tmp_db.save_audit("hello", "2.12.1", "report2", "summary2", "claude")
    tmp_db.save_findings(audit_id_1, [{"category": "a", "severity": "high", "title": "first"}])
    tmp_db.save_findings(audit_id_2, [{"category": "b", "severity": "low", "title": "second"}])
    findings_1 = tmp_db.get_findings_for_audit(audit_id_1)
    findings_2 = tmp_db.get_findings_for_audit(audit_id_2)
    assert len(findings_1) == 1
    assert findings_1[0]["title"] == "first"
    assert len(findings_2) == 1
    assert findings_2[0]["title"] == "second"


def test_save_audit_with_findings_atomic(tmp_db):
    """save_audit(findings=...) saves audit and findings in one transaction."""
    tmp_db.upsert_package("hello", "2.12.1")
    findings = [
        {"category": "supply_chain", "severity": "high", "title": "No hash pinning"},
        {"category": "runtime", "severity": "low", "title": "Large closure"},
    ]
    audit_id = tmp_db.save_audit(
        "hello", "2.12.1", "report", "summary", "claude", findings=findings
    )
    saved = tmp_db.get_findings_for_audit(audit_id)
    assert len(saved) == 2
    assert saved[0]["title"] == "No hash pinning"
    assert saved[1]["title"] == "Large closure"


def test_save_audit_without_findings_param(tmp_db):
    """save_audit without findings= still works (no findings inserted)."""
    tmp_db.upsert_package("hello", "2.12.1")
    audit_id = tmp_db.save_audit("hello", "2.12.1", "report", "summary", "vulnix")
    saved = tmp_db.get_findings_for_audit(audit_id)
    assert saved == []


def test_migrate_adds_missing_columns(tmp_path):
    """Migration should add columns that don't exist in older schema."""
    import sqlite3

    from nix_audit.models.database import AuditDatabase

    db_path = tmp_path / "old.db"
    # Create a minimal old-style schema missing some columns
    conn = sqlite3.connect(str(db_path))
    conn.executescript("""\
        CREATE TABLE packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            version TEXT NOT NULL
        );
        CREATE TABLE audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL REFERENCES packages(id),
            version_audited TEXT NOT NULL,
            date TEXT NOT NULL DEFAULT (datetime('now')),
            report_markdown TEXT NOT NULL
        );
        CREATE TABLE findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER NOT NULL REFERENCES audits(id),
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL
        );
    """)
    conn.close()

    # Opening the DB with AuditDatabase should migrate
    db = AuditDatabase(db_path=db_path)
    # Check that missing columns were added
    pkg_cols = {row[1] for row in db.conn.execute("PRAGMA table_info(packages)").fetchall()}
    assert "store_path" in pkg_cols
    assert "first_seen" in pkg_cols

    audit_cols = {row[1] for row in db.conn.execute("PRAGMA table_info(audits)").fetchall()}
    assert "findings_summary" in audit_cols
    assert "audit_type" in audit_cols

    finding_cols = {row[1] for row in db.conn.execute("PRAGMA table_info(findings)").fetchall()}
    assert "detail" in finding_cols
    assert "recommendation" in finding_cols
    db.close()
