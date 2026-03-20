{ pkgs, ... }:

{
  home.packages = with pkgs; [
    bat                       # Cat with syntax highlighting
    eza                       # Replacement for ls
    fzf                       # Fuzzy finder
    lazydocker                # Simple terminal UI for docker
    lazygit                   # Simple terminal UI for git
    ripgrep                   # Faster grep
    tldr                      # Community-maintained help pages
    yazi                      # TUI File System Manager
  ];
}
