{ ... }:

{
  programs.alacritty = {
    enable = true;
    settings = {
      general.import = [ "~/.config/alacritty/theme.toml" ];

      window = {
        opacity = 0.9;
        padding = {
          x = 5;
          y = 5;
        };
      };

      font.normal.family = "MesloLGS Nerd Font";
    };
  };
}
