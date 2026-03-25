{ lib, config, pkgs, ... }:

let
  cfg = config.andrewos.networking.wireless;
in {
  options.andrewos.networking.wireless = {
    enable = lib.mkEnableOption "IWD wireless networking";
  };

  config = lib.mkIf cfg.enable {
    environment.systemPackages = [ pkgs.impala pkgs.iwd ];
    networking.networkmanager.enable = false;
    networking.wireless.enable = false;
    networking.wireless.iwd.enable = true;
    networking.wireless.iwd.settings = {
      Settings.AutoConnect = true;
      General.EnableNetworkConfiguration = true;
      General.DNS = "systemd";
    };
    networking.dhcpcd.enable = false;
    boot.kernel.sysctl."net.ipv6.conf.default.use_tempaddr" = 2;
    hardware.enableRedistributableFirmware = true;
  };
}
