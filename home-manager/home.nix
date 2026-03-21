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

  _module.args.theme = theme;

  imports = [
    ./scripts.nix
    ./applications/alacritty.nix
    ./applications/chromium.nix
    ./applications/claude-code.nix
    ./applications/notion.nix
    ./applications/obsidian.nix
    ./applications/pavucontrol.nix
    ./applications/wlogout.nix
    ./terminal/btop.nix
    ./dev/cli-tools.nix
    ./shell/direnv.nix
    ./dev/git.nix
    ./editor/lsps.nix
    ./editor/neovim.nix
    ./shell/starship.nix
    ./terminal/tmux.nix
    ./shell/zsh.nix
    theme.neovimModule
  ] ++ (if desktop == "sway" then [
    ./desktop/fuzzel.nix
    ./desktop/sway.nix
    ./desktop/swaync.nix
    ./desktop/waybar.nix
  ] else []);

  # Applications
  andrewos.applications = {
    alacritty.enable = true;
    chromium.enable = true;
    claude-code.enable = true;
    notion.enable = true;
    obsidian.enable = true;
    pavucontrol.enable = true;
    wlogout.enable = true;
  };

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
    ".config/swaync/style.css".source = theme.swaync;
  } else {});

}
