{ pkgs, userConfig, desktop ? "", ... }:

let
  username = userConfig.username;
  theme = import ./../themes/default.nix { inherit pkgs; };
in

{

  home.username = username;
  home.homeDirectory = "/home/${username}";
  home.stateVersion = "24.11";
  programs.home-manager.enable = true;

  imports = [
    ./alacritty.nix
    ./git.nix
    ./neovim.nix
    ./tmux.nix
    ./zsh.nix
    theme.neovimModule
  ];

  programs.direnv = {
    enable = true;
    nix-direnv.enable = true;
  };

  # Hide apps from Fuzzel launcher
  xdg.desktopEntries = {
    nvim = {
      name = "Neovim wrapper";
      noDisplay = true;
    };
    yazi = {
      name = "Yazi";
      noDisplay = true;
    };
  };

  home.packages = with pkgs; [

    # Command line
    bat                       # Cat with syntax highlighting
    eza                       # Replacement for ls
    fzf                       # Fuzzy finder
    lazydocker                # Simple terminal UI for docker
    lazygit                   # Simple terminal UI for git
    ripgrep                   # Faster grep
    starship                  # Prompt
    tldr                      # Community-maintained help pages
    yazi                      # TUI File System Manager

    # Language Server Protocols (LSPs)
    lua-language-server       # Lua
    nil                       # Nix
    pyright                   # Python

  ];

  # Dotfiles that are always loaded
  home.file = {
    ".config/starship.toml".source = ./../dotfiles/starship/starship.toml;
    ".config/nvim/init.lua".source = ./../dotfiles/neovim/init.lua;
    ".config/nvim/lua".source = ./../dotfiles/neovim/lua;
    # Theme configs
    ".config/nvim/theme.lua".source = theme.neovimLua;
    ".config/alacritty/theme.toml".source = theme.alacritty;
  }
  # Sway-specific dotfiles (only loaded when desktop = "sway")
  // (if desktop == "sway" then {
    ".config/sway/config".source = ./../dotfiles/sway/config;
    ".config/sway/theme".source = theme.sway;
    ".config/waybar/config".source = ./../dotfiles/waybar/config;
    ".config/waybar/style.css".source = theme.waybar;
    ".config/fuzzel/fuzzel.ini".source = ./../dotfiles/fuzzel/fuzzel.ini;
    ".config/fuzzel/theme.ini".source = theme.fuzzel;
  } else {});

}
