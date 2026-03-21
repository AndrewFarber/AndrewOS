{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.bat.enable = lib.mkEnableOption "Cat with syntax highlighting";

  config = lib.mkIf config.andrewos.dev.bat.enable {
    home.packages = [ pkgs.bat ];
  };
}
