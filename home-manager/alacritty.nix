{ pkgs, ... }:

{
  programs.alacritty = {
    enable = true;
    settings = {
      general.import = [ "~/.config/alacritty/theme.toml" ];

      window = {
        opacity = 0.9;
        padding = {
          x = 10;
          y = 10;
        };
      };

      font.normal.family = "MesloLGS Nerd Font";
    };
  };
}
