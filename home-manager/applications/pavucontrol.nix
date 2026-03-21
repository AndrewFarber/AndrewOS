{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.pavucontrol.enable = lib.mkEnableOption "PulseAudio Volume Control";

  config = lib.mkIf config.andrewos.applications.pavucontrol.enable {
    home.packages = with pkgs; [
      pavucontrol
    ];

    xdg.desktopEntries.pavucontrol = {
      name = "PulseAudio Volume Control";
      noDisplay = true;
    };
  };
}
