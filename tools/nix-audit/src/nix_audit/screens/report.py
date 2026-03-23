from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown


class ReportScreen(Screen):
    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False),
        Binding("k", "scroll_up", "Up", show=False),
        Binding("g", "scroll_home", "Top", show=False),
        Binding("G", "scroll_end", "Bottom", show=False, priority=True),
        Binding("escape", "go_back", "Back"),
        Binding("q", "go_back", "Back"),
    ]

    def __init__(self, report: str):
        super().__init__()
        self.report = report

    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown(self.report, id="report-content")
        yield Footer()

    def action_scroll_down(self) -> None:
        self.query_one("#report-content", Markdown).scroll_down()

    def action_scroll_up(self) -> None:
        self.query_one("#report-content", Markdown).scroll_up()

    def action_scroll_home(self) -> None:
        self.query_one("#report-content", Markdown).scroll_home()

    def action_scroll_end(self) -> None:
        self.query_one("#report-content", Markdown).scroll_end()

    def action_go_back(self) -> None:
        self.app.pop_screen()
