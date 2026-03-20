{ lib, config, pkgs, ... }:

with lib;
let
  cfg = config.andrewos.networking.wireless;
in {
  options.andrewos.networking.wireless = {
    enable = mkEnableOption "IWD wireless networking";
  };

  config = mkIf cfg.enable {
    environment.systemPackages = [ pkgs.impala pkgs.iwd ];
    networking.networkmanager.enable = false;
    networking.wireless.enable = false;
    networking.wireless.iwd.enable = true;
    networking.wireless.iwd.settings = {
      Settings.AutoConnect = true;
      General.EnableNetworkConfiguration = true;
      General.DNS = "systemd";
    };
    hardware.enableRedistributableFirmware = true;
  };
}
