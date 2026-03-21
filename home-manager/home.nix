{ pkgs, userConfig, desktop ? "", ... }:

let
  username = userConfig.username;
  theme = import ../themes/default.nix { inherit pkgs userConfig; };
in

{

  home.username = username;
  home.homeDirectory = "/home/${username}";
  home.stateVersion = "24.11";
  programs.home-manager.enable = true;

  home.pointerCursor = {
    name = "Adwaita";
    package = pkgs.adwaita-icon-theme;
    size = 24;
    gtk.enable = true;
  };

  _module.args.theme = theme;

  imports = [
    ./applications/claude-code.nix
    ./terminal/btop.nix
    ./dev
    ./shell/direnv.nix
    ./editor/lsps.nix
    ./editor/neovim.nix
    ./shell/starship.nix
    ./terminal/tmux.nix
    ./shell/zsh.nix
    theme.neovimModule
  ] ++ (if desktop != "" then [
    ./desktop
  ] else []);

  andrewos.applications = {
    claude-code.enable = true;
  };

  andrewos.dev = {
    bat.enable = true;
    eza.enable = true;
    fzf.enable = true;
    lazydocker.enable = true;
    lazygit.enable = true;
    pulsemixer.enable = true;
    ripgrep.enable = true;
    tldr.enable = true;
    yazi.enable = true;
  };

  home.file = {
    ".config/nvim/init.lua".source = ../neovim/init.lua;
    ".config/nvim/lua".source = ../neovim/lua;
    ".config/nvim/theme.lua".source = theme.neovimLua;
    ".config/alacritty/theme.toml".source = theme.alacritty;
  };

}
