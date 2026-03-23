import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import DataTable, Footer, Header, Static

from nix_audit.services.claude import run_claude_audit
from nix_audit.services.derivation import get_derivation_source
from nix_audit.services.vulnix import format_vulnix_report, scan_package

log = logging.getLogger(__name__)


class ConfirmAuditScreen(ModalScreen[bool]):
    """Modal dialog to confirm running an audit."""

    BINDINGS = [
        Binding("y", "confirm", "Yes", priority=True),
        Binding("n", "cancel", "No", priority=True),
        Binding("escape", "cancel", "Cancel", priority=True),
    ]

    def __init__(self, package_name: str):
        super().__init__()
        self.package_name = package_name

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Static(
                f"Run security audit on [bold]{self.package_name}[/bold]?\n\n"
                "This will run Claude and Vulnix scans.\n\n"
                "[ansi_green]y[/] Yes  [ansi_red]n[/] No",
            )

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)


class DetailScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False, priority=True),
        Binding("k", "cursor_up", "Up", show=False, priority=True),
        Binding("a", "run_audit", "Audit Package", priority=True),
        Binding("enter", "view_report", "View Report", priority=True),
        Binding("escape", "go_back", "Go Back", priority=True),
        Binding("q", "go_back", "Go Back", show=False, priority=True),
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

    def action_run_audit(self) -> None:
        self.app.push_screen(
            ConfirmAuditScreen(self.package_name),
            self._on_confirm_audit,
        )

    def _on_confirm_audit(self, confirmed: bool) -> None:
        if confirmed:
            self.run_worker(
                self._audit_worker(), exclusive=True, exit_on_error=False
            )

    async def _audit_worker(self) -> None:
        status = self.query_one("#action-status", Static)
        db = self.app.db
        pkg = db.get_package(self.package_name)
        if not pkg:
            db.upsert_package(self.package_name, "unknown")
            pkg = db.get_package(self.package_name)
        version = pkg["version"]
        store_path = pkg.get("store_path")

        reports = []
        self.loading = True

        # Claude audit
        status.update("[ansi_yellow]Fetching derivation source...[/]")
        source = await get_derivation_source(self.package_name)
        if source:
            status.update("[ansi_yellow]Running Claude audit...[/]")
            try:
                result = await run_claude_audit(self.package_name, version, source)
                report_md = result["report_markdown"]
                risk = result["risk_level"]
                n_findings = len(result.get("findings", []))
                summary = f"{risk} -- {n_findings} finding(s)"
                audit_id = db.save_audit(
                    self.package_name, version, report_md, summary, "claude"
                )
                db.save_findings(audit_id, result.get("findings", []))
                reports.append(report_md)
            except Exception as e:
                log.error("Claude audit failed for %s: %s", self.package_name, e)
                self.notify(f"Claude audit failed: {e}", severity="error")
        else:
            self.notify(
                "Could not fetch derivation source, skipping Claude audit",
                severity="warning",
            )

        # Vulnix scan
        if store_path:
            status.update("[ansi_yellow]Running Vulnix CVE scan...[/]")
            try:
                cves = await scan_package(store_path)
                report = format_vulnix_report(cves, self.package_name, version)
                summary = f"{len(cves)} CVE(s) found" if cves else "No CVEs found"
                db.save_audit(
                    self.package_name, version, report, summary, "vulnix"
                )
                reports.append(report)
            except Exception as e:
                log.error("Vulnix scan failed for %s: %s", self.package_name, e)
                self.notify(f"Vulnix scan failed: {e}", severity="error")
        else:
            self.notify(
                "No store path available, skipping Vulnix scan",
                severity="warning",
            )

        self.loading = False
        self._refresh_audits()
        status.update("[ansi_green]Audit complete[/]")

        if reports:
            combined = "\n\n---\n\n".join(reports)
            from nix_audit.screens.report import ReportScreen

            self.app.push_screen(ReportScreen(combined))

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
