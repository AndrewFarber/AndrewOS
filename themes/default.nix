{ pkgs }:

let
  theme = "gruvbox";  # Change this one line to switch themes

  # Auto-pick the first background (0-*) from the theme's backgrounds directory
  backgroundsDir = ./${theme}/backgrounds;
  backgroundFiles = builtins.filter (name: builtins.match "0-.*" name != null)
    (builtins.attrNames (builtins.readDir backgroundsDir));
  wallpaper = backgroundsDir + "/${builtins.head backgroundFiles}";

  # Hyprlock colors per theme (RGB values without # prefix)
  hyprlockColors = {
    "tokyo-night" = {
      background = "rgb(24, 25, 38)";
      accent = "rgb(122, 162, 247)";
      inner = "rgb(36, 40, 59)";
      font = "rgb(192, 202, 245)";
    };
    "gruvbox" = {
      background = "rgb(40, 40, 40)";
      accent = "rgb(125, 174, 163)";
      inner = "rgb(60, 56, 54)";
      font = "rgb(212, 190, 152)";
    };
  };
in
{
  name = theme;

  # Neovim
  neovimModule = import ./${theme}/neovim.nix;
  neovimLua = ./${theme}/colorscheme.lua;

  # Terminal
  alacritty = ./${theme}/alacritty.toml;

  # Desktop (sway)
  sway = ./${theme}/sway;
  fuzzel = ./${theme}/fuzzel.ini;
  waybar = ./${theme}/waybar.css;

  # Wallpaper
  inherit wallpaper;

  # Hyprlock
  hyprlock = hyprlockColors.${theme};
}
