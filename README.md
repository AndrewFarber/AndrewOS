# AndrewOS

Personal [NixOS](https://nixos.org/) and [Home Manager](https://nix-community.github.io/home-manager/) configurations for a reproducible Linux development environment.

## Features

- **Declarative System Configuration** - Entire system defined in Nix, easily reproducible
- **Sway Desktop** - Wayland tiling window manager with waybar, fuzzel, and swaync
- **Theme System** - Switchable themes (tokyo-night, gruvbox) affecting terminal, editor, desktop
- **Comprehensive Development Setup** - Neovim with LSP, Git integration, and debugging support
- **Modular Architecture** - Pluggable modules for bootloaders, drivers, desktops, and user config
- **Headless Support** - SSH access for running in VirtualBox without GUI

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
   cd nixos/hosts/vbox-desktop
   rm hardware.nix
   nixos-generate-config --dir .
   mv hardware-configuration.nix hardware.nix
   rm configuration.nix
   cd ~/AndrewOS
   ```
5. Edit `user.nix` with your settings:
   ```nix
   {
     username = "yourname";
     fullName = "Your Name";
     email = "you@example.com";
     theme = "gruvbox";
     timezone = "America/Los_Angeles";
   }
   ```
6. Build and switch:
   ```bash
   sudo nixos-rebuild switch --flake .#vbox-desktop   # or .#thinkpad-x1
   ```
7. Reboot

See detailed instructions in [nixos/hosts/README.md](./nixos/hosts/README.md).

## Configuration

Edit `user.nix` at the repository root to set your personal information:

| Field      | Description                          |
|------------|--------------------------------------|
| `username` | System username                      |
| `fullName` | Full name (for Git)                  |
| `email`    | Email (for Git)                      |
| `theme`    | Active theme (`tokyo-night`, `gruvbox`) |
| `timezone` | System timezone (e.g. `America/Los_Angeles`) |

## Development Environments

### Jupyter Lab

Scientific Python environment with NumPy, Pandas, Matplotlib, scikit-learn, and more:

```bash
jupyter  # alias to enter Jupyter dev shell
```

## Common Commands

After installation, these shell aliases are available:

| Command   | Description                              |
|-----------|------------------------------------------|
| `rebuild` | Rebuild NixOS configuration              |
| `update`  | Update flake inputs                      |
| `gc`      | Run garbage collection                   |
| `jupyter` | Enter Jupyter development shell          |
| `lg`      | Launch Lazygit                           |
| `ld`      | Launch Lazydocker                        |
| `y`       | Launch Yazi file manager                 |

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
