{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.yazi.enable = lib.mkEnableOption "TUI file system manager";

  config = lib.mkIf config.andrewos.dev.yazi.enable {
    home.packages = [ pkgs.yazi ];
  };
}
