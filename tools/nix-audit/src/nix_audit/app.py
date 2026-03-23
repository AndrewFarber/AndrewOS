import logging
import os
from pathlib import Path

from textual.app import App

from nix_audit.models.database import AuditDatabase
from nix_audit.screens.packages import PackagesScreen

LOG_DIR = Path(
    os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))
) / "nix-audit"
LOG_FILE = LOG_DIR / "nix-audit.log"


def setup_logging() -> None:
    """Configure file-based logging for the entire app."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class NixAuditApp(App):
    TITLE = "nix-audit"
    SUB_TITLE = "Nix Package Security Auditor"
    CSS_PATH = "style.tcss"
    ENABLE_COMMAND_PALETTE = False

    ansi_color = True

    def __init__(self):
        super().__init__()
        self.db = AuditDatabase()

    def on_mount(self) -> None:
        self.push_screen(PackagesScreen())

    def on_unmount(self) -> None:
        self.db.close()


def main():
    setup_logging()
    logging.getLogger("nix_audit").info("nix-audit starting")
    app = NixAuditApp()
    app.run()
    logging.getLogger("nix_audit").info("nix-audit exiting")
