import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input, Static

from nix_audit.services.nix import get_installed_packages

log = logging.getLogger(__name__)


class PackagesScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False, priority=True),
        Binding("k", "cursor_up", "Up", show=False, priority=True),
        Binding("g", "cursor_first", "First", show=False, priority=True),
        Binding("G", "cursor_last", "Last", show=False, priority=True),
        Binding("enter", "select_package", "Package Detail", priority=True),
        Binding("escape", "dismiss_filter", "Dismiss Filter", show=False, priority=True),
        Binding("slash", "open_filter", "Filter Packages"),
        Binding("r", "refresh", "Refresh List"),
        Binding("question_mark", "show_help", "Show Help"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Loading packages...", id="status-bar")
        yield Input(placeholder="Filter packages...", id="filter-input")
        yield DataTable(id="packages-table")
        yield Footer()

    def on_mount(self) -> None:
        self._all_rows: list[tuple] = []
        filter_input = self.query_one("#filter-input", Input)
        filter_input.display = False
        table = self.query_one("#packages-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("Status", "Name", "Version", "Last Audited")
        self.load_packages()

    def load_packages(self) -> None:
        self.run_worker(self._load_packages_worker(), exclusive=True, exit_on_error=False)

    async def _load_packages_worker(self) -> None:
        status = self.query_one("#status-bar", Static)
        status.update("Loading packages...")
        try:
            packages = await get_installed_packages()
        except Exception as e:
            log.error("Failed to load packages: %s", e)
            status.update(f"Error: {e}")
            return
        db = self.app.db
        table = self.query_one("#packages-table", DataTable)
        table.clear()
        db.upsert_packages_batch(packages)
        audit_info = db.get_all_audit_info()
        self._all_rows = []
        for pkg in packages:
            info = audit_info.get(pkg["name"], {})
            audit_status = info.get("status", "none")
            last_audited = info.get("last_audited", "never")
            if audit_status == "current":
                indicator = "[ansi_green]\u25cf[/]"
            elif audit_status == "outdated":
                indicator = "[ansi_yellow]\u25cf[/]"
            else:
                indicator = "[ansi_red]\u25cb[/]"
            row = (indicator, pkg["name"], pkg["version"], last_audited)
            self._all_rows.append(row)
            table.add_row(*row)
        status.update(f"{len(packages)} packages loaded")
        table.focus()

    def _apply_filter(self, query: str) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.clear()
        query_lower = query.lower()
        for row in self._all_rows:
            if query_lower in row[1].lower():
                table.add_row(*row)

    def on_input_changed(self, event: Input.Changed) -> None:
        self._apply_filter(event.value)

    def action_open_filter(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        filter_input.display = True
        filter_input.focus()

    def action_dismiss_filter(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        if not filter_input.display:
            return
        filter_input.value = ""
        filter_input.display = False
        self._apply_filter("")
        self.query_one("#packages-table", DataTable).focus()

    def action_cursor_down(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        table.action_cursor_up()

    def action_cursor_first(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.move_cursor(row=0)

    def action_cursor_last(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        table.move_cursor(row=table.row_count - 1)

    def action_select_package(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        if filter_input.has_focus:
            filter_input.display = False
            table = self.query_one("#packages-table", DataTable)
            if table.row_count > 0:
                table.focus()
            return
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        row_idx = table.cursor_row
        row = table.get_row_at(row_idx)
        # row is [status, name, version, last_audited]
        name = row[1]
        from nix_audit.screens.detail import DetailScreen

        self.app.push_screen(DetailScreen(package_name=str(name)))

    def action_quit(self) -> None:
        self.app.exit()

    def action_refresh(self) -> None:
        self.load_packages()

    def action_show_help(self) -> None:
        self.notify(
            "j/k: navigate  Enter: detail  /: filter  Esc: clear  r: refresh  q: quit",
            title="Keybindings",
        )
