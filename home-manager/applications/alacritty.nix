{ config, lib, ... }:

{
  options.andrewos.applications.alacritty.enable = lib.mkEnableOption "Alacritty terminal emulator";

  config = lib.mkIf config.andrewos.applications.alacritty.enable {
    programs.alacritty = {
      enable = true;
      settings = {
        general.import = [ "~/.config/alacritty/theme.toml" ];

        window = {
          opacity = 0.85;
          padding = {
            x = 5;
            y = 5;
          };
        };

        font.normal.family = "MesloLGS Nerd Font";
      };
    };
  };
}
