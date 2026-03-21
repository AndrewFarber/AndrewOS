{ desktop, theme, ... }:

{
  imports = [
    ../scripts.nix
    ../applications/alacritty.nix
    ../applications/chatgpt.nix
    ../applications/chromium.nix
    ../applications/claude.nix
    ../applications/figma.nix
    ../applications/github.nix
    ../applications/linear.nix
    ../applications/notion.nix

    ../applications/pavucontrol.nix
    ../applications/proton-pass.nix
    ../applications/wlogout.nix
  ] ++ (if desktop == "sway" then [
    ./fuzzel.nix
    ./sway.nix
    ./swaync.nix
    ./waybar.nix
  ] else []);

  andrewos.applications = {
    alacritty.enable = true;
    chatgpt.enable = true;
    chromium.enable = true;
    claude.enable = true;
    figma.enable = true;
    github.enable = true;
    linear.enable = true;
    notion.enable = true;

    pavucontrol.enable = true;
    proton-pass.enable = true;
    wlogout.enable = true;
  };

  # Hide system desktop entries from the app launcher
  xdg.desktopEntries.nixos-manual = {
    name = "NixOS Manual";
    noDisplay = true;
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
