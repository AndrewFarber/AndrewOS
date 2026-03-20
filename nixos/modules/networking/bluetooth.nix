{ lib, config, pkgs, ... }:

with lib;
let
  cfg = config.andrewos.networking.bluetooth;
in {
  options.andrewos.networking.bluetooth = {
    enable = mkEnableOption "Bluetooth support";
  };

  config = mkIf cfg.enable {
    hardware.bluetooth.enable = true;
    hardware.bluetooth.powerOnBoot = true;
  };
}
