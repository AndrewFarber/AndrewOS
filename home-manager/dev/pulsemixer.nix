{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.pulsemixer.enable = lib.mkEnableOption "TUI audio mixer";

  config = lib.mkIf config.andrewos.dev.pulsemixer.enable {
    home.packages = [ pkgs.pulsemixer ];
  };
}
