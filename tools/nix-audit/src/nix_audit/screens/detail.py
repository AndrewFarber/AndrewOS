import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from nix_audit.services.claude import run_claude_audit
from nix_audit.services.derivation import get_derivation_source
from nix_audit.services.vulnix import format_vulnix_report, scan_package

log = logging.getLogger(__name__)


class DetailScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("a", "run_claude_audit", "Claude Audit"),
        Binding("v", "run_vulnix", "Vulnix Scan"),
        Binding("enter", "view_report", "View Report"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "go_back", "Back"),
    ]

    def __init__(self, package_name: str):
        super().__init__()
        self.package_name = package_name

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="pkg-info")
        yield Static("Audit History:", classes="section-title")
        yield DataTable(id="audit-table")
        yield Static("", id="action-status")
        yield Footer()

    def on_mount(self) -> None:
        db = self.app.db
        pkg = db.get_package(self.package_name)
        info = self.query_one("#pkg-info", Static)
        if pkg:
            info.update(
                f"[bold]{self.package_name}[/bold] v{pkg['version']}\n"
                f"Store: {pkg.get('store_path', 'N/A')}"
            )
        else:
            info.update(f"[bold]{self.package_name}[/bold] (not installed)")

        table = self.query_one("#audit-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("Date", "Version", "Type", "Summary")
        self._refresh_audits()

    def _refresh_audits(self) -> None:
        db = self.app.db
        table = self.query_one("#audit-table", DataTable)
        table.clear()
        audits = db.get_audits_for_package(self.package_name)
        for audit in audits:
            summary = audit.get("findings_summary") or "(no summary)"
            if len(summary) > 50:
                summary = summary[:50] + "..."
            table.add_row(
                audit["date"],
                audit["version_audited"],
                audit["audit_type"],
                summary,
            )

    def action_cursor_down(self) -> None:
        self.query_one("#audit-table", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#audit-table", DataTable).action_cursor_up()

    def action_run_claude_audit(self) -> None:
        self.run_worker(self._claude_audit_worker(), exclusive=True)

    async def _claude_audit_worker(self) -> None:
        status = self.query_one("#action-status", Static)
        status.update("[ansi_yellow]Fetching derivation source...[/]")
        source = await get_derivation_source(self.package_name)
        if not source:
            status.update("[ansi_red]Could not fetch derivation source[/]")
            return
        status.update("[ansi_yellow]Running Claude audit (this may take a minute)...[/]")
        db = self.app.db
        pkg = db.get_package(self.package_name)
        if not pkg:
            db.upsert_package(self.package_name, "unknown")
            pkg = db.get_package(self.package_name)
        version = pkg["version"]
        try:
            report = await run_claude_audit(self.package_name, version, source)
        except RuntimeError as e:
            log.error("Claude audit failed for %s: %s", self.package_name, e)
            status.update(f"[ansi_red]Audit failed: {e}[/]")
            return
        # Extract first line as summary
        first_line = report.strip().splitlines()[0] if report.strip() else ""
        summary = first_line[:100]
        db.save_audit(self.package_name, version, report, summary, "claude")
        self._refresh_audits()
        status.update("[ansi_green]Claude audit complete[/]")
        from nix_audit.screens.report import ReportScreen
        self.app.push_screen(ReportScreen(report))

    def action_run_vulnix(self) -> None:
        self.run_worker(self._vulnix_worker(), exclusive=True)

    async def _vulnix_worker(self) -> None:
        status = self.query_one("#action-status", Static)
        db = self.app.db
        pkg = db.get_package(self.package_name)
        if not pkg or not pkg.get("store_path"):
            status.update("[ansi_red]No store path available for vulnix scan[/]")
            return
        status.update("[ansi_yellow]Running vulnix CVE scan...[/]")
        try:
            cves = await scan_package(pkg["store_path"])
        except Exception as e:
            log.error("Vulnix scan failed for %s: %s", self.package_name, e)
            status.update(f"[ansi_red]Vulnix scan failed: {e}[/]")
            return
        report = format_vulnix_report(cves, self.package_name, pkg["version"])
        summary = f"{len(cves)} CVE(s) found" if cves else "No CVEs found"
        db.save_audit(self.package_name, pkg["version"], report, summary, "vulnix")
        self._refresh_audits()
        status.update(f"[ansi_green]Vulnix scan complete: {summary}[/]")
        from nix_audit.screens.report import ReportScreen
        self.app.push_screen(ReportScreen(report))

    def action_view_report(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        if table.row_count == 0:
            return
        db = self.app.db
        audits = db.get_audits_for_package(self.package_name)
        row_idx = table.cursor_row
        if row_idx < len(audits):
            report = audits[row_idx]["report_markdown"]
            from nix_audit.screens.report import ReportScreen
            self.app.push_screen(ReportScreen(report))

    def action_go_back(self) -> None:
        self.app.pop_screen()
