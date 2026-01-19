# HydraOS

Personal [NixOS](https://nixos.org/) and [Home Manager](https://nix-community.github.io/home-manager/) configurations for a reproducible Linux development environment.

## Features

- **Declarative System Configuration** - Entire system defined in Nix, easily reproducible
- **Multiple Desktop Environments** - Sway (Wayland), GNOME, or Plasma 6
- **Comprehensive Development Setup** - Neovim with LSP, Git integration, and debugging support
- **Modular Architecture** - Pluggable modules for bootloaders, drivers, desktops, and user config
- **Headless Support** - SSH access for running in VirtualBox without GUI

## Directory Structure

```
HydraOS/
├── home-manager/            # User environment modules
│   ├── alacritty.nix        # Terminal emulator
│   ├── cli-tools.nix        # CLI tools (bat, eza, fzf, etc.)
│   ├── direnv.nix           # Direnv configuration
│   ├── fuzzel.nix           # Application launcher
│   ├── git.nix              # Git configuration
│   ├── home.nix             # Main home-manager entry
│   ├── lsps.nix             # Language servers
│   ├── neovim.nix           # Editor configuration
│   ├── starship.nix         # Shell prompt
│   ├── sway.nix             # Window manager
│   ├── tmux.nix             # Terminal multiplexer
│   ├── waybar.nix           # Status bar
│   └── zsh.nix              # Shell configuration
├── neovim/                  # Neovim Lua configuration
│   ├── init.lua
│   └── lua/
├── nixos/
│   ├── hosts/
│   │   ├── vbox-laptop/     # VirtualBox laptop config
│   │   └── vbox-desktop/    # VirtualBox desktop config
│   └── modules/
│       ├── bootloaders/     # Systemd boot configuration
│       ├── core/            # Network, users, packages, fonts
│       ├── desktops/        # Sway, GNOME, Plasma 6 configs
│       └── drivers/         # VirtualBox graphics drivers
├── themes/                  # Theme configurations
├── shells/
│   └── jupyter.nix          # Jupyter Lab dev environment
├── assets/
│   └── bookmarks.html       # Browser bookmarks
├── flake.nix                # Nix flakes entry point
└── flake.lock               # Locked dependencies
```

## Technologies

### Core
- NixOS 24.11
- Home Manager
- Nix Flakes
- Systemd

### Desktop (Sway Stack)
- Sway (Wayland compositor)
- Waybar (status bar)
- Fuzzel (launcher)
- Alacritty (terminal)
- Mako (notifications)
- Tuigreet (login manager)

### Development
- **Editor**: Neovim with Treesitter, LSP (Lua, Nix, Python), Telescope, Harpoon
- **Shell**: Zsh with Starship prompt
- **Terminal**: Alacritty, Tmux
- **Git**: Lazygit, gh CLI, gitsigns
- **Tools**: Ripgrep, Bat, Eza, FZF, Yazi

### Applications
- Chromium (with Vimium, Proton Pass)
- Obsidian
- Claude Code

## Installation

### Prerequisites

- Oracle VirtualBox
- NixOS graphical ISO
- 6GB+ RAM, 50GB+ disk, 2+ CPU cores

### Setup

1. Create VirtualBox VM and boot NixOS ISO
2. Install NixOS using graphical installer
3. Clone repository:
   ```bash
   git clone https://github.com/AndrewFarber/AndrewOS
   cd AndrewOS
   ```
4. Generate hardware configuration:
   ```bash
   nixos-generate-config --dir .
   ```
5. Copy and configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your USERNAME, NAME, and EMAIL
   ```
6. Build and switch:
   ```bash
   source .env && sudo -E nixos-rebuild switch --flake .#vbox --impure
   ```
7. Reboot

See detailed instructions in [nixos/hosts/vbox/README.md](./nixos/hosts/vbox/README.md).

## Configuration

Copy `.env.example` to `.env` and set your personal information:

```bash
cp .env.example .env
```

| Variable   | Description          |
|------------|----------------------|
| `USERNAME` | System username      |
| `NAME`     | Full name (for Git)  |
| `EMAIL`    | Email (for Git)      |

This file is gitignored to keep personal data out of version control.

## Desktop Environments

Three desktop options are available:

| Desktop  | Type    | Description                     |
|----------|---------|---------------------------------|
| Sway     | Wayland | Tiling WM, primary config       |
| GNOME    | Wayland | Full desktop environment        |
| Plasma 6 | Wayland | KDE desktop environment         |

## Development Environments

### Jupyter Lab

Scientific Python environment with NumPy, Pandas, Matplotlib, scikit-learn, and more:

```bash
jupyter  # alias to enter Jupyter shell
```

## Common Commands

After installation, these aliases are available:

| Command   | Description                              |
|-----------|------------------------------------------|
| `rebuild` | Rebuild NixOS configuration              |
| `gc`      | Run garbage collection                   |
| `update`  | Update flake inputs                      |
| `jupyter` | Enter Jupyter development shell          |
| `lg`      | Launch Lazygit                           |
| `ld`      | Launch Lazydocker                        |

Manual rebuild command:

```bash
source .env && sudo -E nixos-rebuild switch --flake .#vbox --impure
```

## Headless Operation

For running VirtualBox VM without GUI (e.g., on Windows host):

1. Enable SSH port forwarding:
   ```bash
   VBoxManage modifyvm "NixOS" --natpf1 "SSH,tcp,,2222,,22"
   ```

2. Start VM headlessly:
   ```bash
   VBoxManage startvm "NixOS" --type headless
   ```

3. Connect via SSH:
   ```bash
   ssh -p 2222 user@localhost
   ```

## License

Personal configuration - feel free to use as reference for your own setup.
