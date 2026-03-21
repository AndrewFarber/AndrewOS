{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.figma.enable = lib.mkEnableOption "Figma";

  config = lib.mkIf config.andrewos.applications.figma.enable {
    xdg.desktopEntries.figma = {
      name = "Figma";
      comment = "Figma design tool";
      exec = "${pkgs.chromium}/bin/chromium --app=https://www.figma.com";
      icon = "${../../assets/icons/figma.png}";
      terminal = false;
      categories = [ "Graphics" ];
    };
  };
}
