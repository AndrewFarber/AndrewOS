{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.lazydocker.enable = lib.mkEnableOption "Simple terminal UI for docker";

  config = lib.mkIf config.andrewos.dev.lazydocker.enable {
    home.packages = [ pkgs.lazydocker ];
  };
}
