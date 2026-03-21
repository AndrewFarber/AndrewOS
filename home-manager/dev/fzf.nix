{ config, lib, pkgs, ... }:

{
  options.andrewos.dev.fzf.enable = lib.mkEnableOption "Fuzzy finder";

  config = lib.mkIf config.andrewos.dev.fzf.enable {
    home.packages = [ pkgs.fzf ];
  };
}
