{ config, lib, ... }:

{
  options.andrewos.applications.linear.enable = lib.mkEnableOption "Linear";

  config = lib.mkIf config.andrewos.applications.linear.enable {
    xdg.desktopEntries.linear = {
      name = "Linear";
      comment = "Linear project management";
      exec = "andrewos-launch-linear";
      icon = "${../../assets/icons/linear.png}";
      terminal = false;
      categories = [ "Office" ];
    };
  };
}
