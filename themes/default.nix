{ pkgs }:

let
  theme = "tokyo-night";  # Change this one line to switch themes
in
{
  name = theme;

  # Neovim
  neovimModule = import ./${theme}/neovim.nix;
  neovimLua = ./${theme}/tokyonight.lua;

  # Terminal
  alacritty = ./${theme}/alacritty.toml;

  # Desktop (sway)
  sway = ./${theme}/sway;
  fuzzel = ./${theme}/fuzzel.ini;
  waybar = ./${theme}/waybar.css;

  # Wallpaper
  wallpaper = ./${theme}/backgrounds/default.png;
}
