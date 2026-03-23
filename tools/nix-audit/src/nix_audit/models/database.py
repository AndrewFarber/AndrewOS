import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "nix-audit" / "audit.db"

SCHEMA = """\
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    version TEXT NOT NULL,
    store_path TEXT,
    first_seen TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL REFERENCES packages(id),
    version_audited TEXT NOT NULL,
    date TEXT NOT NULL DEFAULT (datetime('now')),
    report_markdown TEXT NOT NULL,
    findings_summary TEXT,
    audit_type TEXT NOT NULL DEFAULT 'claude'
);
"""


class AuditDatabase:
    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    def _migrate(self):
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def upsert_package(self, name: str, version: str, store_path: str | None = None):
        self.conn.execute(
            """\
            INSERT INTO packages (name, version, store_path)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                version = excluded.version,
                store_path = excluded.store_path,
                last_seen = datetime('now')
            """,
            (name, version, store_path),
        )
        self.conn.commit()

    def get_package(self, name: str) -> dict | None:
        row = self.conn.execute(
            "SELECT * FROM packages WHERE name = ?", (name,)
        ).fetchone()
        return dict(row) if row else None

    def get_all_packages(self) -> list[dict]:
        rows = self.conn.execute(
            "SELECT * FROM packages ORDER BY name"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_audit_status(self, name: str) -> str:
        """Return 'none', 'current', or 'outdated'."""
        pkg = self.get_package(name)
        if not pkg:
            return "none"
        audit = self.conn.execute(
            """\
            SELECT version_audited FROM audits
            WHERE package_id = ?
            ORDER BY date DESC LIMIT 1
            """,
            (pkg["id"],),
        ).fetchone()
        if not audit:
            return "none"
        return "current" if audit["version_audited"] == pkg["version"] else "outdated"

    def save_audit(
        self,
        package_name: str,
        version: str,
        report_markdown: str,
        findings_summary: str | None = None,
        audit_type: str = "claude",
    ):
        pkg = self.get_package(package_name)
        if not pkg:
            raise ValueError(f"Package {package_name!r} not found in database")
        self.conn.execute(
            """\
            INSERT INTO audits (package_id, version_audited, report_markdown, findings_summary, audit_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (pkg["id"], version, report_markdown, findings_summary, audit_type),
        )
        self.conn.commit()

    def get_audits_for_package(self, package_name: str) -> list[dict]:
        pkg = self.get_package(package_name)
        if not pkg:
            return []
        rows = self.conn.execute(
            """\
            SELECT * FROM audits
            WHERE package_id = ?
            ORDER BY date DESC
            """,
            (pkg["id"],),
        ).fetchall()
        return [dict(r) for r in rows]
