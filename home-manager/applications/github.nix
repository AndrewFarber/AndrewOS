{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.github.enable = lib.mkEnableOption "GitHub";

  config = lib.mkIf config.andrewos.applications.github.enable {
    xdg.desktopEntries.github = {
      name = "GitHub";
      comment = "GitHub";
      exec = "${pkgs.chromium}/bin/chromium --app=https://github.com";
      icon = "${../../assets/icons/github.png}";
      terminal = false;
      categories = [ "Development" ];
    };
  };
}
