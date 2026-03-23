import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, RichLog, Static

from nix_audit.screens.help import AUDIT_HELP, HelpScreen
from nix_audit.services.claude import stream_claude_audit
from nix_audit.services.vulnix import format_vulnix_report, scan_package

log = logging.getLogger(__name__)

HALF_PAGE_LINES = 15


class AuditScreen(Screen):
    """Screen that streams Claude audit output in real-time."""

    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False, priority=True),
        Binding("k", "scroll_up", "Up", show=False, priority=True),
        Binding("ctrl+d", "page_down", "Page Down", show=False, priority=True),
        Binding("ctrl+u", "page_up", "Page Up", show=False, priority=True),
        Binding("g", "scroll_home", "Top", show=False, priority=True),
        Binding("G", "scroll_end", "Bottom", show=False, priority=True),
        Binding("v", "view_report", "View Report", priority=True),
        Binding("question_mark", "show_help", "Show Help"),
        Binding("escape", "go_back", "Go Back", priority=True),
        Binding("q", "go_back", "Go Back", show=False, priority=True),
    ]

    def __init__(
        self,
        package_name: str,
        version: str,
        derivation_source: str,
        store_path: str | None = None,
        nixpkgs_attr: str | None = None,
    ):
        super().__init__()
        self.package_name = package_name
        self.version = version
        self.derivation_source = derivation_source
        self.store_path = store_path
        self.nixpkgs_attr = nixpkgs_attr
        self._report: str | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"[bold]Auditing {self.package_name} {self.version}[/bold]",
            id="audit-info",
        )
        yield RichLog(id="audit-log", wrap=True, markup=True)
        yield Static("[ansi_yellow]Streaming Claude output...[/]", id="audit-status")
        yield Footer()

    def on_mount(self) -> None:
        self.run_worker(self._run_audit(), exclusive=True, exit_on_error=False)

    async def _run_audit(self) -> None:
        rich_log = self.query_one("#audit-log", RichLog)
        status = self.query_one("#audit-status", Static)
        db = self.app.db
        reports: list[str] = []

        # Stream Claude audit with line callback
        def _on_line(line: str) -> None:
            rich_log.write(line.rstrip("\n"))

        try:
            result = await stream_claude_audit(
                self.package_name,
                self.version,
                self.derivation_source,
                on_line=_on_line,
            )
        except RuntimeError as e:
            log.error("Claude audit failed for %s: %s", self.package_name, e)
            status.update(f"[ansi_red]Claude audit failed: {e}[/]")
            self.notify(f"Claude audit failed: {e}", severity="error")
            return

        report_md = result["report_markdown"]
        risk = result["risk_level"]
        n_findings = len(result.get("findings", []))
        summary = f"{risk} -- {n_findings} finding(s)"
        db.save_audit(
            self.package_name,
            self.version,
            report_md,
            summary,
            "claude",
            findings=result.get("findings", []),
        )
        reports.append(report_md)

        # Vulnix scan
        if self.store_path:
            status.update("[ansi_yellow]Running Vulnix CVE scan...[/]")
            try:
                cves = await scan_package(self.store_path)
                report = format_vulnix_report(cves, self.package_name, self.version)
                vuln_summary = f"{len(cves)} CVE(s) found" if cves else "No CVEs found"
                db.save_audit(
                    self.package_name,
                    self.version,
                    report,
                    vuln_summary,
                    "vulnix",
                )
                reports.append(report)
            except Exception as e:
                log.error("Vulnix scan failed for %s: %s", self.package_name, e)
                self.notify(f"Vulnix scan failed: {e}", severity="error")

        if reports:
            self._report = "\n\n---\n\n".join(reports)
            status.update("[ansi_green]Audit complete. Press [bold]v[/bold] to view report.[/]")
        else:
            status.update("[ansi_red]No reports generated.[/]")

    def action_scroll_down(self) -> None:
        self.query_one("#audit-log", RichLog).scroll_down()

    def action_scroll_up(self) -> None:
        self.query_one("#audit-log", RichLog).scroll_up()

    def action_page_down(self) -> None:
        rl = self.query_one("#audit-log", RichLog)
        rl.scroll_to(y=rl.scroll_y + HALF_PAGE_LINES, animate=False)

    def action_page_up(self) -> None:
        rl = self.query_one("#audit-log", RichLog)
        rl.scroll_to(y=max(rl.scroll_y - HALF_PAGE_LINES, 0), animate=False)

    def action_scroll_home(self) -> None:
        self.query_one("#audit-log", RichLog).scroll_home()

    def action_scroll_end(self) -> None:
        self.query_one("#audit-log", RichLog).scroll_end()

    def action_view_report(self) -> None:
        if self._report:
            from nix_audit.screens.report import ReportScreen

            self.app.push_screen(ReportScreen(self._report))
        else:
            self.notify("No report available yet.", severity="warning")

    def action_show_help(self) -> None:
        self.app.push_screen(HelpScreen("Audit", AUDIT_HELP))

    def action_go_back(self) -> None:
        self.app.pop_screen()
