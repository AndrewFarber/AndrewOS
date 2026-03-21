{ config, lib, ... }:

{
  options.andrewos.applications.github.enable = lib.mkEnableOption "GitHub";

  config = lib.mkIf config.andrewos.applications.github.enable {
    xdg.desktopEntries.github = {
      name = "GitHub";
      comment = "GitHub";
      exec = "andrewos-launch-github";
      icon = "${../../assets/icons/github.png}";
      terminal = false;
      categories = [ "Development" ];
    };
  };
}
