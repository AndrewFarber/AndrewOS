# AndrewOS

My [NixOS](https://nixos.org/) and [Home-Manager](https://nix-community.github.io/home-manager/) configurations.

Home-Manager can be used within a NixOS environment or part of a standalone Nix installation.


## Configuration

Copy `.env.example` to `.env` and update with your user settings:

```bash
cp .env.example .env
```

This file is gitignored and keeps your personal information out of version control.


## Common Commands

Commands require sourcing the `.env` file and the `--impure` flag:

```bash
source .env && sudo -E nixos-rebuild switch --flake .#vbox --impure
source .env && home-manager switch --flake . --impure
nix-collect-garbage
home-manager expire-generations
home-manager generations
home-manager rollback
```

## Environments

### NixOS within Oracle VirtualBox

See instllation instructions [here](./nixos/hosts/vbox).

### Home-Manager (Standalone)

Home-Manager can be installed on any Linux distribution or as a standalone setup.

- Install `MesloLG` [Nerd Font](https://www.nerdfonts.com/font-downloads)
- Install [Nix](https://nixos.org/).
  - Add `experimental-features = nix-command flakes` to `/etc/nix/nix.conf` file.
- Install [Home-Manager](https://nix-community.github.io/home-manager/).
  ```shell
  nix-channel --add https://github.com/nix-community/home-manager/archive/master.tar.gz home-manager
  nix-channel --update
  nix-shell '<home-manager>' -A install
  ```
