{ desktop, theme, ... }:

{
  imports = [
    ../scripts.nix
    ../applications/alacritty.nix
    ../applications/chromium.nix
    ../applications/notion.nix
    ../applications/obsidian.nix
    ../applications/pavucontrol.nix
    ../applications/wlogout.nix
  ] ++ (if desktop == "sway" then [
    ./fuzzel.nix
    ./sway.nix
    ./swaync.nix
    ./waybar.nix
  ] else []);

  andrewos.applications = {
    alacritty.enable = true;
    chromium.enable = true;
    notion.enable = true;
    obsidian.enable = true;
    pavucontrol.enable = true;
    wlogout.enable = true;
  };

  # Desktop theme files (except alacritty theme.toml which stays in home.nix)
  home.file = if desktop == "sway" then {
    ".config/sway/theme".source = theme.sway;
    ".config/sway/wallpaper".source = theme.wallpaper;
    ".config/waybar/style.css".source = theme.waybar;
    ".config/fuzzel/theme.ini".source = theme.fuzzel;
    ".config/swaync/style.css".source = theme.swaync;
  } else {};
}
