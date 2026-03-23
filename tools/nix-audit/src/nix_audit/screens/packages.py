import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from nix_audit.services.nix import get_installed_packages

log = logging.getLogger(__name__)


class PackagesScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("g", "cursor_first", "First", show=False),
        Binding("G", "cursor_last", "Last", show=False, priority=True),
        Binding("enter", "select_package", "Detail"),
        Binding("slash", "open_search", "Search"),
        Binding("r", "refresh", "Refresh"),
        Binding("question_mark", "show_help", "Help"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Loading packages...", id="status-bar")
        yield DataTable(id="packages-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("Status", "Name", "Version", "Last Audited")
        self.load_packages()

    def load_packages(self) -> None:
        self.run_worker(self._load_packages_worker(), exclusive=True)

    async def _load_packages_worker(self) -> None:
        status = self.query_one("#status-bar", Static)
        status.update("Loading packages...")
        try:
            packages = await get_installed_packages()
        except RuntimeError as e:
            log.error("Failed to load packages: %s", e)
            status.update(f"Error: {e}")
            return
        db = self.app.db
        table = self.query_one("#packages-table", DataTable)
        table.clear()
        db.upsert_packages_batch(packages)
        audit_info = db.get_all_audit_info()
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
            table.add_row(indicator, pkg["name"], pkg["version"], last_audited)
        status.update(f"{len(packages)} packages loaded")

    def action_cursor_down(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.action_cursor_up()

    def action_cursor_first(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.move_cursor(row=0)

    def action_cursor_last(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.move_cursor(row=table.row_count - 1)

    def action_select_package(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        row_idx = table.cursor_row
        row = table.get_row_at(row_idx)
        # row is [status, name, version, last_audited]
        name = row[1]
        from nix_audit.screens.detail import DetailScreen
        self.app.push_screen(DetailScreen(package_name=str(name)))

    def action_open_search(self) -> None:
        from nix_audit.screens.search import SearchScreen
        self.app.push_screen(SearchScreen())

    def action_refresh(self) -> None:
        self.load_packages()

    def action_show_help(self) -> None:
        self.notify(
            "j/k: navigate  Enter: detail  /: search  r: refresh  q: quit",
            title="Keybindings",
        )
