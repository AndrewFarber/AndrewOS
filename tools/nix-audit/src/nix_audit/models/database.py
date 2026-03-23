import logging
import sqlite3
from pathlib import Path

log = logging.getLogger(__name__)

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

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id INTEGER NOT NULL REFERENCES audits(id),
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    detail TEXT,
    recommendation TEXT
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

    # Expected columns per table for forward migration.
    # Format: {table: {column: "TYPE [DEFAULT ...]"}}
    _EXPECTED_COLUMNS: dict[str, dict[str, str]] = {
        "packages": {
            "store_path": "TEXT",
            "first_seen": "TEXT NOT NULL DEFAULT (datetime('now'))",
            "last_seen": "TEXT NOT NULL DEFAULT (datetime('now'))",
        },
        "audits": {
            "findings_summary": "TEXT",
            "audit_type": "TEXT NOT NULL DEFAULT 'claude'",
        },
        "findings": {
            "detail": "TEXT",
            "recommendation": "TEXT",
        },
    }

    def _migrate(self):
        self.conn.executescript(SCHEMA)
        self.conn.commit()
        # Add any columns that are missing from existing tables
        for table, columns in self._EXPECTED_COLUMNS.items():
            existing = {
                row[1] for row in self.conn.execute(f"PRAGMA table_info({table})").fetchall()
            }
            for col_name, col_def in columns.items():
                if col_name not in existing:
                    log.info("Migrating: adding column %s.%s", table, col_name)
                    self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}")
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
                store_path = COALESCE(excluded.store_path, packages.store_path),
                last_seen = datetime('now')
            """,
            (name, version, store_path),
        )
        self.conn.commit()

    def upsert_packages_batch(self, packages: list[dict]):
        """Upsert many packages in a single transaction."""
        with self.conn:
            self.conn.executemany(
                """\
                INSERT INTO packages (name, version, store_path)
                VALUES (:name, :version, :store_path)
                ON CONFLICT(name) DO UPDATE SET
                    version = excluded.version,
                    store_path = COALESCE(excluded.store_path, packages.store_path),
                    last_seen = datetime('now')
                """,
                packages,
            )

    def get_package(self, name: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM packages WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None

    def get_all_packages(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM packages ORDER BY name").fetchall()
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
        findings: list[dict] | None = None,
    ) -> int:
        """Save an audit (and optional findings) atomically. Returns the audit id."""
        pkg = self.get_package(package_name)
        if not pkg:
            log.error("Attempted to save audit for unknown package %r", package_name)
            raise ValueError(f"Package {package_name!r} not found in database")
        with self.conn:
            cursor = self.conn.execute(
                """\
                INSERT INTO audits
                    (package_id, version_audited, report_markdown, findings_summary, audit_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pkg["id"], version, report_markdown, findings_summary, audit_type),
            )
            audit_id = cursor.lastrowid
            if findings:
                self._insert_findings(audit_id, findings)
        return audit_id

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

    def _insert_findings(self, audit_id: int, findings: list[dict]):
        """Insert findings rows (caller must manage transaction)."""
        for f in findings:
            self.conn.execute(
                """\
                INSERT INTO findings
                    (audit_id, category, severity, title, detail, recommendation)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    f.get("category", "unknown"),
                    f.get("severity", "info"),
                    f.get("title", ""),
                    f.get("detail", ""),
                    f.get("recommendation"),
                ),
            )

    def save_findings(self, audit_id: int, findings: list[dict]):
        """Save structured findings linked to the given audit."""
        with self.conn:
            self._insert_findings(audit_id, findings)

    def get_findings_for_audit(self, audit_id: int) -> list[dict]:
        """Get all structured findings for a given audit."""
        rows = self.conn.execute(
            "SELECT * FROM findings WHERE audit_id = ? ORDER BY id",
            (audit_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_all_audit_info(self) -> dict[str, dict]:
        """Get audit status and last-audited date for all packages in one query.

        Returns {name: {"status": str, "last_audited": str}}.
        """
        rows = self.conn.execute(
            """\
            SELECT
                p.name,
                p.version,
                a.version_audited,
                a.date AS last_date
            FROM packages p
            LEFT JOIN (
                SELECT package_id, version_audited, date,
                       ROW_NUMBER() OVER (PARTITION BY package_id ORDER BY date DESC) AS rn
                FROM audits
            ) a ON a.package_id = p.id AND a.rn = 1
            """,
        ).fetchall()
        result = {}
        for row in rows:
            row = dict(row)
            if row["version_audited"] is None:
                status = "none"
                last_audited = "never"
            elif row["version_audited"] == row["version"]:
                status = "current"
                last_audited = row["last_date"]
            else:
                status = "outdated"
                last_audited = row["last_date"]
            result[row["name"]] = {"status": status, "last_audited": last_audited}
        return result
