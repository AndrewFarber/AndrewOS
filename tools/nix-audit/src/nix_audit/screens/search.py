import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Input

from nix_audit.screens.help import SEARCH_HELP, HelpScreen
from nix_audit.services.nix import search_packages

log = logging.getLogger(__name__)


class SearchScreen(Screen):
    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False, priority=True),
        Binding("k", "cursor_up", "Up", show=False, priority=True),
        Binding("ctrl+d", "page_down", "Page Down", show=False, priority=True),
        Binding("ctrl+u", "page_up", "Page Up", show=False, priority=True),
        Binding("g", "cursor_first", "First", show=False, priority=True),
        Binding("G", "cursor_last", "Last", show=False, priority=True),
        Binding("enter", "submit_or_select", "Select", priority=True),
        Binding("slash", "focus_input", "New Search"),
        Binding("question_mark", "show_help", "Show Help"),
        Binding("escape", "escape", "Go Back", priority=True),
        Binding("q", "go_back", "Go Back", show=False, priority=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search nixpkgs (Enter to search)...", id="search-input")
        yield DataTable(id="search-results")
        yield Footer()

    def on_mount(self) -> None:
        self._results: list[dict] = []
        table = self.query_one("#search-results", DataTable)
        table.cursor_type = "row"
        table.add_columns("Name", "Version", "Description")
        self.query_one("#search-input", Input).focus()

    def _do_search(self) -> None:
        query = self.query_one("#search-input", Input).value.strip()
        if query:
            self.run_worker(self._search_worker(query), exclusive=True, exit_on_error=False)

    async def _search_worker(self, query: str) -> None:
        table = self.query_one("#search-results", DataTable)
        table.clear()
        self._results = []
        try:
            results = await search_packages(query)
        except Exception as e:
            log.error("Search failed for %r: %s", query, e)
            self.notify(f"Search failed: {e}", severity="error")
            return
        self._results = results
        for pkg in results:
            desc = pkg["description"]
            if len(desc) > 60:
                desc = desc[:60] + "..."
            table.add_row(pkg["name"], pkg["version"], desc)
        if results:
            table.focus()

    HALF_PAGE = 15

    def action_cursor_down(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        table.action_cursor_up()

    def action_page_down(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        target = min(table.cursor_row + self.HALF_PAGE, table.row_count - 1)
        table.move_cursor(row=target)

    def action_page_up(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        target = max(table.cursor_row - self.HALF_PAGE, 0)
        table.move_cursor(row=target)

    def action_cursor_first(self) -> None:
        table = self.query_one("#search-results", DataTable)
        table.move_cursor(row=0)

    def action_cursor_last(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        table.move_cursor(row=table.row_count - 1)

    def action_submit_or_select(self) -> None:
        search_input = self.query_one("#search-input", Input)
        if search_input.has_focus:
            self._do_search()
            return
        # Table focused: select result
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        row_idx = table.cursor_row
        if row_idx >= len(self._results):
            return
        pkg = self._results[row_idx]
        from nix_audit.screens.detail import DetailScreen

        self.app.push_screen(DetailScreen(
            package_name=pkg["name"],
            version=pkg["version"],
            nixpkgs_attr=pkg.get("nixpkgs_attr"),
        ))

    def action_focus_input(self) -> None:
        self.query_one("#search-input", Input).focus()

    def action_escape(self) -> None:
        search_input = self.query_one("#search-input", Input)
        if search_input.has_focus:
            table = self.query_one("#search-results", DataTable)
            if table.row_count > 0:
                # Results exist: focus table instead of leaving
                table.focus()
                return
        self.app.pop_screen()

    def action_show_help(self) -> None:
        self.app.push_screen(HelpScreen("Search", SEARCH_HELP))

    def action_go_back(self) -> None:
        self.app.pop_screen()
