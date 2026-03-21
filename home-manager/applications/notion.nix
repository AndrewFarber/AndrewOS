{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.notion.enable = lib.mkEnableOption "Notion";

  config = lib.mkIf config.andrewos.applications.notion.enable {
    xdg.desktopEntries.notion = {
      name = "Notion";
      comment = "Notion workspace";
      exec = "${pkgs.chromium}/bin/chromium --app=https://www.notion.so";
      icon = "${../../assets/icons/notion.png}";
      terminal = false;
      categories = [ "Office" ];
    };
  };
}
