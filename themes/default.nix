{ pkgs, userConfig }:

let
  theme = userConfig.theme or "tokyo-night";

  # Auto-pick the first background (0-*) from the theme's backgrounds directory
  backgroundsDir = ./${theme}/backgrounds;
  backgroundFiles = builtins.filter (name: builtins.match "0-.*" name != null)
    (builtins.attrNames (builtins.readDir backgroundsDir));
  wallpaper = backgroundsDir + "/${builtins.head backgroundFiles}";

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

  # btop
  btopTheme = {
    "tokyo-night" = "tokyo-night";
    "gruvbox" = "gruvbox_material_dark";
  }.${theme};
}
