# AndrewOS

My [NixOS](https://nixos.org/) and [Home-Manager](https://nix-community.github.io/home-manager/) configurations.


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
nix-collect-garbage
```

After the first rebuild, you can use the `rebuild` alias from anywhere.


## Installation

### NixOS within Oracle VirtualBox

See installation instructions [here](./nixos/hosts/vbox).
