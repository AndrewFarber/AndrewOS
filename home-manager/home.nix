{ pkgs, userConfig, desktop ? "", ... }:

let
  username = userConfig.username;
  theme = import ../themes/default.nix { inherit pkgs; };
in

{

  home.username = username;
  home.homeDirectory = "/home/${username}";
  home.stateVersion = "24.11";
  programs.home-manager.enable = true;

  imports = [
    ./alacritty.nix
    ./cli-tools.nix
    ./direnv.nix
    ./git.nix
    ./lsps.nix
    ./neovim.nix
    ./starship.nix
    ./tmux.nix
    ./zsh.nix
    theme.neovimModule
  ] ++ (if desktop == "sway" then [
    ./fuzzel.nix
    ./sway.nix
    ./waybar.nix
  ] else if desktop == "hyprland" then [
    ./fuzzel.nix
    ./hyprland.nix
    ./waybar.nix
  ] else []);

  # Dotfiles that are always loaded
  home.file = {
    ".config/nvim/init.lua".source = ../neovim/init.lua;
    ".config/nvim/lua".source = ../neovim/lua;
    # Theme configs
    ".config/nvim/theme.lua".source = theme.neovimLua;
    ".config/alacritty/theme.toml".source = theme.alacritty;
  }
  # Sway-specific theme files (only loaded when desktop = "sway")
  // (if desktop == "sway" then {
    ".config/sway/theme".source = theme.sway;
    ".config/sway/wallpaper".source = theme.wallpaper;
    ".config/waybar/style.css".source = theme.waybar;
    ".config/fuzzel/theme.ini".source = theme.fuzzel;
  } else {})
  # Hyprland theme files (reuses waybar and fuzzel themes)
  // (if desktop == "hyprland" then {
    ".config/waybar/style.css".source = theme.waybar;
    ".config/fuzzel/theme.ini".source = theme.fuzzel;
    ".config/hypr/wallpaper".source = theme.wallpaper;
  } else {});

}
