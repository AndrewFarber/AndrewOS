{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.tldr.enable = lib.mkEnableOption "Community-maintained help pages";

  config = lib.mkIf config.andrewos.dev.tldr.enable {
    home.packages = [ pkgs.tldr ];
  };
}
