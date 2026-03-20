{ lib, config, ... }:

with lib;
let
  cfg = config.andrewos.bootloader.systemd;
in {

  options.andrewos.bootloader.systemd = {
    enable = mkEnableOption "systemd-boot";
  };

  config = mkIf cfg.enable {
    boot.loader.systemd-boot.enable = true;
    boot.loader.systemd-boot.configurationLimit = 15;
    boot.loader.efi.canTouchEfiVariables = true;
  };

}
