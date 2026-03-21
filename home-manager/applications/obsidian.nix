{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.obsidian.enable = lib.mkEnableOption "Obsidian note-taking app";

  config = lib.mkIf config.andrewos.applications.obsidian.enable {
    home.packages = with pkgs; [
      obsidian
    ];
  };
}
