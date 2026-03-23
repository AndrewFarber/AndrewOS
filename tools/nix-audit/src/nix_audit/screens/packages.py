import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input, Static

from nix_audit.screens.help import PACKAGES_HELP, HelpScreen
from nix_audit.services.nix import get_installed_packages

log = logging.getLogger(__name__)


class PackagesScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False, priority=True),
        Binding("k", "cursor_up", "Up", show=False, priority=True),
        Binding("ctrl+d", "page_down", "Page Down", show=False, priority=True),
        Binding("ctrl+u", "page_up", "Page Up", show=False, priority=True),
        Binding("g", "cursor_first", "First", show=False, priority=True),
        Binding("G", "cursor_last", "Last", show=False, priority=True),
        Binding("enter", "select_package", "Package Detail", priority=True),
        Binding("escape", "dismiss_filter", "Dismiss Filter", show=False, priority=True),
        Binding("slash", "open_filter", "Filter Packages"),
        Binding("S", "search_nixpkgs", "Search Nixpkgs", priority=True),
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

    def on_screen_resume(self) -> None:
        """Refresh audit status when returning from detail/report screens."""
        self._refresh_audit_status()

    def _refresh_audit_status(self) -> None:
        """Re-read audit info from DB and update table rows without reloading packages."""
        if not self._all_rows:
            return
        db = self.app.db
        audit_info = db.get_all_audit_info()
        new_rows = []
        for row in self._all_rows:
            name = row[1]
            version = row[2]
            info = audit_info.get(name, {})
            audit_status = info.get("status", "none")
            last_audited = info.get("last_audited", "never")
            if audit_status == "current":
                indicator = "[ansi_green]\u25cf[/]"
            elif audit_status == "outdated":
                indicator = "[ansi_yellow]\u25cf[/]"
            else:
                indicator = "[ansi_red]\u25cb[/]"
            new_rows.append((indicator, name, version, last_audited))
        self._all_rows = new_rows
        # Re-apply current filter (or show all)
        filter_input = self.query_one("#filter-input", Input)
        self._apply_filter(filter_input.value if filter_input.value else "")

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
        # Re-apply active filter if one is set
        filter_input = self.query_one("#filter-input", Input)
        if filter_input.display and filter_input.value:
            self._apply_filter(filter_input.value)
        table.focus()

    def _apply_filter(self, query: str) -> None:
        table = self.query_one("#packages-table", DataTable)
        table.clear()
        query_lower = query.lower()
        for row in self._all_rows:
            if query_lower in row[1].lower():
                table.add_row(*row)

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "filter-input":
            self._apply_filter(event.value)

    def action_open_filter(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        filter_input.display = True
        filter_input.focus()

    def _confirm_filter(self) -> None:
        """Hide filter input, keep filtered results, focus table."""
        filter_input = self.query_one("#filter-input", Input)
        filter_input.display = False
        table = self.query_one("#packages-table", DataTable)
        table.focus()
        if filter_input.value:
            self.query_one("#status-bar", Static).update(
                f"Filter: \"{filter_input.value}\" ({table.row_count} matches) — Escape to clear"
            )

    def _clear_filter(self) -> None:
        """Clear filter, restore full list."""
        filter_input = self.query_one("#filter-input", Input)
        filter_input.value = ""
        filter_input.display = False
        self._apply_filter("")
        self.query_one("#status-bar", Static).update(
            f"{len(self._all_rows)} packages loaded"
        )

    def action_dismiss_filter(self) -> None:
        filter_input = self.query_one("#filter-input", Input)
        if filter_input.has_focus:
            # From input: confirm filter, keep results, focus table
            self._confirm_filter()
            return
        if filter_input.value:
            # From table with active filter: clear filter, restore full list
            self._clear_filter()
            return

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

    HALF_PAGE = 15

    def action_page_down(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        target = min(table.cursor_row + self.HALF_PAGE, table.row_count - 1)
        table.move_cursor(row=target)

    def action_page_up(self) -> None:
        table = self.query_one("#packages-table", DataTable)
        if table.row_count == 0:
            return
        target = max(table.cursor_row - self.HALF_PAGE, 0)
        table.move_cursor(row=target)

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
            # Confirm filter and focus table (don't open detail yet)
            self._confirm_filter()
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

    def action_search_nixpkgs(self) -> None:
        from nix_audit.screens.search import SearchScreen

        self.app.push_screen(SearchScreen())

    def action_show_help(self) -> None:
        self.app.push_screen(HelpScreen("Packages", PACKAGES_HELP))
