from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static


class HelpScreen(ModalScreen[None]):
    """Modal overlay showing keybindings for the current context."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", priority=True),
        Binding("q", "dismiss", "Close", show=False, priority=True),
        Binding("question_mark", "dismiss", "Close", show=False, priority=True),
    ]

    def __init__(self, context: str, bindings_text: str):
        super().__init__()
        self.context = context
        self.bindings_text = bindings_text

    def compose(self) -> ComposeResult:
        with Vertical(id="help-dialog"):
            yield Static(
                f"[bold]Keybindings — {self.context}[/bold]\n\n"
                f"{self.bindings_text}\n\n"
                "[dim]Press Escape or q to close[/dim]"
            )


PACKAGES_HELP = (
    "[bold]Navigation[/bold]\n"
    "  j / k         Move down / up\n"
    "  Ctrl+d / u    Page down / up\n"
    "  g / G         Jump to first / last\n"
    "\n[bold]Actions[/bold]\n"
    "  Enter         Open package detail\n"
    "  /             Filter packages\n"
    "  Escape        Dismiss filter\n"
    "  S             Search nixpkgs\n"
    "  r             Refresh list\n"
    "  ?             Show this help\n"
    "  q             Quit"
)

DETAIL_HELP = (
    "[bold]Navigation[/bold]\n"
    "  j / k         Move down / up\n"
    "  Ctrl+d / u    Page down / up\n"
    "  g / G         Jump to first / last\n"
    "\n[bold]Actions[/bold]\n"
    "  Enter         View audit report\n"
    "  a             Run security audit\n"
    "  s             Save source files\n"
    "  e             Open in Neovim\n"
    "  ?             Show this help\n"
    "  Escape / q    Go back"
)

REPORT_HELP = (
    "[bold]Navigation[/bold]\n"
    "  j / k         Scroll down / up\n"
    "  Ctrl+d / u    Page down / up\n"
    "  g / G         Scroll to top / bottom\n"
    "\n[bold]Actions[/bold]\n"
    "  ?             Show this help\n"
    "  Escape / q    Go back"
)

SEARCH_HELP = (
    "[bold]Navigation[/bold]\n"
    "  j / k         Move down / up\n"
    "  Ctrl+d / u    Page down / up\n"
    "  g / G         Jump to first / last\n"
    "\n[bold]Actions[/bold]\n"
    "  Enter         Open package detail\n"
    "  ?             Show this help\n"
    "  Escape / q    Go back"
)
