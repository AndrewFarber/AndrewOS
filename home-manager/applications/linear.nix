{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.linear.enable = lib.mkEnableOption "Linear (Chromium web app)";

  config = lib.mkIf config.andrewos.applications.linear.enable {
    xdg.desktopEntries.linear = {
      name = "Linear";
      comment = "Linear project management";
      exec = "${pkgs.chromium}/bin/chromium --app=https://linear.app";
      icon = "${../../assets/icons/linear.png}";
      terminal = false;
      categories = [ "Office" ];
    };
  };
}
