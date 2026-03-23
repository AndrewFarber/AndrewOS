# nix-audit

Nix package security audit TUI built with Python/Textual.

## Development

```bash
cd tools/nix-audit
# direnv auto-loads the nix dev shell (use flake ../..#nix-audit)
just test        # run all tests
just run         # launch the TUI
just lint        # ruff check + format check
just fmt         # auto-fix lint + format
```

If direnv isn't available, use: `nix develop .#nix-audit --command bash`

## Project Layout

```
src/
  nix_audit/
    app.py                  # NixAuditApp(textual.App), entry point
    style.tcss              # Textual CSS — ANSI colors only
    screens/
      packages.py           # Main screen: installed package list
      search.py             # nix search interface
      detail.py             # Package info + audit history
      report.py             # Full report display (Markdown)
    widgets/
      search_bar.py         # Input with debounced search
    models/
      database.py           # SQLite operations (~/.local/share/nix-audit/audit.db)
    services/
      nix.py                # home-manager packages, nix search
      claude.py             # claude -p invocation for security audit
      derivation.py         # Fetch .nix source via nix eval meta.position
      vulnix.py             # vulnix CVE scanner
  tests/
    conftest.py             # Shared fixtures (tmp_db, sample data)
    test_database.py
    test_nix_service.py
    test_claude_service.py
    test_derivation_service.py
    test_vulnix_service.py
    test_app.py             # Textual pilot integration tests
```

## Key Patterns

- **ANSI colors only**: `ansi_color = True` on App. All CSS uses `ansi_red`, `ansi_green`, etc. to inherit the terminal theme. Never use hex colors.
- **Async services**: All subprocess calls use `asyncio.create_subprocess_exec` inside Textual workers (`self.run_worker()`).
- **Vim keybindings**: j/k navigate, g/G jump, Enter selects, q/Escape goes back. Defined via `BINDINGS` on each Screen.
- **Tests mock everything**: No real nix/claude/vulnix calls. Patch `asyncio.create_subprocess_exec` in the relevant service module.
- **File logging**: All errors and key events log to `~/.local/share/nix-audit/nix-audit.log` via Python `logging`. Each module uses `log = logging.getLogger(__name__)`.

## Testing

Tests use pytest + pytest-asyncio. All 44 tests should pass:

```bash
just test
```

For Textual app tests, use `async with app.run_test() as pilot:` pattern. Mock `get_installed_packages` before running the app.

## Nix Integration

- `home-manager/applications/nix-audit.nix` — HM module using `buildPythonApplication`
- Enabled in `home-manager/home.nix` under `andrewos.applications.nix-audit.enable`
- Launcher: `bin/andrewos-launch-nix-audit` (floating terminal via `alacritty --class floating-term`)
- Menu entry: Super+D > Tools > Nix Audit

## Adding New Features

- New screens go in `screens/`, register keybindings via `BINDINGS`
- New services go in `services/`, always async, always add corresponding `tests/test_*.py`
- Database schema changes go in `models/database.py` SCHEMA string (auto-migrated via `CREATE TABLE IF NOT EXISTS`)
