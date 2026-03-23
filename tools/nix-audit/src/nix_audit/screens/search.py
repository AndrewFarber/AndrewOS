import logging

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from nix_audit.services.nix import search_packages
from nix_audit.widgets.search_bar import SearchBar

log = logging.getLogger(__name__)


class SearchScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("enter", "select_result", "Detail", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield SearchBar(placeholder="Search nixpkgs...", id="search-input")
        yield DataTable(id="search-results")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#search-results", DataTable)
        table.cursor_type = "row"
        table.add_columns("Name", "Version", "Description")
        self.query_one("#search-input", SearchBar).focus()

    def on_search_bar_submitted(self, event: SearchBar.Submitted) -> None:
        query = event.value.strip()
        if query:
            self.run_worker(self._search_worker(query), exclusive=True, exit_on_error=False)

    async def _search_worker(self, query: str) -> None:
        table = self.query_one("#search-results", DataTable)
        table.clear()
        try:
            results = await search_packages(query)
        except Exception as e:
            log.error("Search failed for %r: %s", query, e)
            self.notify(f"Search failed: {e}", severity="error")
            return
        for pkg in results:
            desc = pkg["description"]
            if len(desc) > 60:
                desc = desc[:60] + "..."
            table.add_row(pkg["name"], pkg["version"], desc)

    def action_select_result(self) -> None:
        table = self.query_one("#search-results", DataTable)
        if table.row_count == 0:
            return
        row_idx = table.cursor_row
        row = table.get_row_at(row_idx)
        name = row[0]
        from nix_audit.screens.detail import DetailScreen
        self.app.push_screen(DetailScreen(package_name=str(name)))

    def action_go_back(self) -> None:
        self.app.pop_screen()
