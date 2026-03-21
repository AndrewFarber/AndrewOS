{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.wlogout.enable = lib.mkEnableOption "wlogout power menu";

  config = lib.mkIf config.andrewos.applications.wlogout.enable {
    home.packages = with pkgs; [
      wlogout
    ];
  };
}
