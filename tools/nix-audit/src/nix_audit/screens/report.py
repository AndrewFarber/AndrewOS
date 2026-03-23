import subprocess
import tempfile

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown

from nix_audit.screens.help import REPORT_HELP, HelpScreen

HALF_PAGE_LINES = 15


class ReportScreen(Screen):
    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False, priority=True),
        Binding("k", "scroll_up", "Up", show=False, priority=True),
        Binding("ctrl+d", "page_down", "Page Down", show=False, priority=True),
        Binding("ctrl+u", "page_up", "Page Up", show=False, priority=True),
        Binding("g", "scroll_home", "Top", show=False, priority=True),
        Binding("G", "scroll_end", "Bottom", show=False, priority=True),
        Binding("e", "open_editor", "Open in Neovim", priority=True),
        Binding("question_mark", "show_help", "Show Help"),
        Binding("escape", "go_back", "Go Back", priority=True),
        Binding("q", "go_back", "Go Back", show=False, priority=True),
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

    def action_page_down(self) -> None:
        md = self.query_one("#report-content", Markdown)
        md.scroll_to(y=md.scroll_y + HALF_PAGE_LINES, animate=False)

    def action_page_up(self) -> None:
        md = self.query_one("#report-content", Markdown)
        md.scroll_to(y=max(md.scroll_y - HALF_PAGE_LINES, 0), animate=False)

    def action_scroll_home(self) -> None:
        self.query_one("#report-content", Markdown).scroll_home()

    def action_scroll_end(self) -> None:
        self.query_one("#report-content", Markdown).scroll_end()

    def action_open_editor(self) -> None:
        with tempfile.NamedTemporaryFile(
            suffix=".md", prefix="nix-audit-report-", mode="w", delete=False
        ) as f:
            f.write(self.report)
            tmp_path = f.name
        with self.app.suspend():
            subprocess.run(["nvim", tmp_path])

    def action_show_help(self) -> None:
        self.app.push_screen(HelpScreen("Report", REPORT_HELP))

    def action_go_back(self) -> None:
        self.app.pop_screen()
