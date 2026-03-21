{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.chromium.enable = lib.mkEnableOption "Chromium web browser";

  config = lib.mkIf config.andrewos.applications.chromium.enable {
    home.packages = with pkgs; [
      chromium
    ];
  };
}
