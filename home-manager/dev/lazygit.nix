{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.lazygit.enable = lib.mkEnableOption "Simple terminal UI for git";

  config = lib.mkIf config.andrewos.dev.lazygit.enable {
    home.packages = [ pkgs.lazygit ];
  };
}
