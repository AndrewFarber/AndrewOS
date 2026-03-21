{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.ripgrep.enable = lib.mkEnableOption "Faster grep";

  config = lib.mkIf config.andrewos.dev.ripgrep.enable {
    home.packages = [ pkgs.ripgrep ];
  };
}
