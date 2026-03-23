import logging
import subprocess

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import DataTable, Footer, Header, Static

from nix_audit.screens.help import DETAIL_HELP, HelpScreen
from nix_audit.services.derivation import (
    get_saved_sources_dir,
    resolve_and_read_source,
    save_derivation_files,
)

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
        Binding("ctrl+d", "page_down", "Page Down", show=False, priority=True),
        Binding("ctrl+u", "page_up", "Page Up", show=False, priority=True),
        Binding("g", "cursor_first", "First", show=False, priority=True),
        Binding("G", "cursor_last", "Last", show=False, priority=True),
        Binding("a", "run_audit", "Audit Package", priority=True),
        Binding("s", "save_source", "Save Source", priority=True),
        Binding("e", "open_editor", "Open in Neovim", priority=True),
        Binding("enter", "view_report", "View Report", priority=True),
        Binding("question_mark", "show_help", "Show Help"),
        Binding("escape", "go_back", "Go Back", priority=True),
        Binding("q", "go_back", "Go Back", show=False, priority=True),
    ]

    def __init__(
        self,
        package_name: str,
        version: str | None = None,
        nixpkgs_attr: str | None = None,
    ):
        super().__init__()
        self.package_name = package_name
        self._init_version = version
        self.nixpkgs_attr = nixpkgs_attr or package_name

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
        # If opened from search with a known version, ensure the DB has it
        if self._init_version and (not pkg or pkg["version"] == "unknown"):
            db.upsert_package(self.package_name, self._init_version)
            pkg = db.get_package(self.package_name)
        info = self.query_one("#pkg-info", Static)
        if pkg:
            store = pkg.get("store_path") or "(not installed)"
            info.update(f"[bold]{self.package_name}[/bold] v{pkg['version']}\nStore: {store}")
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

    HALF_PAGE = 15

    def action_cursor_down(self) -> None:
        self.query_one("#audit-table", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#audit-table", DataTable).action_cursor_up()

    def action_page_down(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        if table.row_count == 0:
            return
        target = min(table.cursor_row + self.HALF_PAGE, table.row_count - 1)
        table.move_cursor(row=target)

    def action_page_up(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        if table.row_count == 0:
            return
        target = max(table.cursor_row - self.HALF_PAGE, 0)
        table.move_cursor(row=target)

    def action_cursor_first(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        table.move_cursor(row=0)

    def action_cursor_last(self) -> None:
        table = self.query_one("#audit-table", DataTable)
        if table.row_count == 0:
            return
        table.move_cursor(row=table.row_count - 1)

    def action_run_audit(self) -> None:
        self.app.push_screen(
            ConfirmAuditScreen(self.package_name),
            self._on_confirm_audit,
        )

    def _on_confirm_audit(self, confirmed: bool) -> None:
        if confirmed:
            self.run_worker(self._audit_worker(), exclusive=True, exit_on_error=False)

    async def _audit_worker(self) -> None:
        status = self.query_one("#action-status", Static)
        db = self.app.db
        pkg = db.get_package(self.package_name)
        if not pkg:
            db.upsert_package(self.package_name, self._init_version or "unknown")
            pkg = db.get_package(self.package_name)
        version = pkg["version"]
        store_path = pkg.get("store_path")

        status.update("[ansi_yellow]Fetching derivation source...[/]")
        source, _saved = await resolve_and_read_source(self.nixpkgs_attr)
        if not source:
            self.notify(
                "Could not fetch derivation source, skipping audit",
                severity="warning",
            )
            status.update("")
            return

        from nix_audit.screens.audit import AuditScreen

        self.app.push_screen(
            AuditScreen(
                package_name=self.package_name,
                version=version,
                derivation_source=source,
                store_path=store_path,
                nixpkgs_attr=self.nixpkgs_attr,
            )
        )
        status.update("")

    def on_screen_resume(self) -> None:
        self._refresh_audits()

    def action_save_source(self) -> None:
        self.run_worker(self._save_source_worker(), exclusive=True, exit_on_error=False)

    async def _save_source_worker(self) -> None:
        status = self.query_one("#action-status", Static)
        status.update("[ansi_yellow]Saving source files...[/]")
        saved = await save_derivation_files(self.nixpkgs_attr)
        if saved:
            status.update(
                f"[ansi_green]Saved {len(saved)} file(s) to sources/{self.package_name}/[/]"
            )
        else:
            status.update("[ansi_red]Could not fetch source files[/]")

    def action_open_editor(self) -> None:
        sources_dir = get_saved_sources_dir(self.package_name)
        if not sources_dir:
            self.notify(
                "No saved source files. Press s to save first.",
                severity="warning",
            )
            return
        files = sorted(sources_dir.glob("*.nix"))
        if not files:
            self.notify(
                "No saved source files. Press s to save first.",
                severity="warning",
            )
            return
        with self.app.suspend():
            subprocess.run(["nvim", *[str(f) for f in files]])

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

    def action_show_help(self) -> None:
        self.app.push_screen(HelpScreen("Package Detail", DETAIL_HELP))

    def action_go_back(self) -> None:
        self.app.pop_screen()
