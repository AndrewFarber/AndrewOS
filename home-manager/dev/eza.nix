{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.eza.enable = lib.mkEnableOption "Replacement for ls";

  config = lib.mkIf config.andrewos.dev.eza.enable {
    home.packages = [ pkgs.eza ];
  };
}
