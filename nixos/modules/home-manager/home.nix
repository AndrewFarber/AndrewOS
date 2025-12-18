{ pkgs, userConfig, ... }:

let
  username = userConfig.username;
in

{

  home.username = "${username}";
  home.homeDirectory = "/home/${username}";
  home.stateVersion = "24.05";
  programs.home-manager.enable = true;

  imports = [
    ./alacritty.nix
    ./git.nix
    ./neovim.nix
    ./tmux.nix
    ./zsh.nix
  ];

  home.packages = with pkgs; [
    
    # Command line
    eza                       # Replacement for ls
    fzf                       # Fuzzy finder
    lazydocker                # Simple terminal UI for docker
    lazygit                   # Simple terminal UI for git
    ripgrep                   # Faster grep
    starship                  # Prompt
    tldr                      # Community-maintained help pages
    yazi                      # TUI File System Manager
    xclip                     # Clipboard

    # Language Server Protocols (LSPs)
    lua-language-server       # Lua
    nil                       # Nix
    pyright                   # Python

  ];

  home.file = {
    ".config/starship.toml".source = ./../../../dotfiles/starship/starship.toml;
    ".config/nvim/init.lua".source = ./../../../dotfiles/neovim/init.lua;
    ".config/nvim/lua".source = ./../../../dotfiles/neovim/lua;
    ".config/alacritty/alacritty.toml".source = ./../../../dotfiles/alacritty/alacritty.toml;
  };

}
