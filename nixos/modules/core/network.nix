{ host, pkgs, ... }:

{
  environment.systemPackages = [ pkgs.impala pkgs.iwd ];
  networking.hostName = host;

  networking.networkmanager.enable = false;
  networking.wireless.enable = false;
  networking.wireless.iwd.enable = true;
  networking.wireless.iwd.settings = {
    Settings.AutoConnect = true;
    General.EnableNetworkConfiguration = true;
    General.DNS = "systemd";
  };
  hardware.enableRedistributableFirmware = true;

  services.resolved.enable = true;

  networking.firewall.enable = true;
  networking.firewall.trustedInterfaces = [ "docker0" ];

  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "no";
      PasswordAuthentication = true;
    };
  };
}
