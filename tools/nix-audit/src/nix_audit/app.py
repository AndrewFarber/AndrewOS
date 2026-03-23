from textual.app import App

from nix_audit.models.database import AuditDatabase
from nix_audit.screens.packages import PackagesScreen


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
    app = NixAuditApp()
    app.run()
