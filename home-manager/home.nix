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
    ./terminal/btop.nix
    ./terminal/alacritty.nix
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
    ./desktop/waybar.nix
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
  } else {});

}
