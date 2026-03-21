{ config, lib, ... }:

{
  options.andrewos.applications.figma.enable = lib.mkEnableOption "Figma";

  config = lib.mkIf config.andrewos.applications.figma.enable {
    xdg.desktopEntries.figma = {
      name = "Figma";
      comment = "Figma design tool";
      exec = "andrewos-launch-figma";
      icon = "${../../assets/icons/figma.png}";
      terminal = false;
      categories = [ "Graphics" ];
    };
  };
}
