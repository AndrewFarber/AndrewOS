{ host, ... }:

{
  networking.hostName = host;
  networking.firewall.enable = true;

  # Use systemd-networkd instead of dhcpcd for DHCP.
  # dhcpcd 10.3.0 has a bug in ipv6nd_expire causing repeated segfaults.
  networking.useDHCP = false;
  networking.useNetworkd = true;
  systemd.network = {
    enable = true;
    networks."10-lan" = {
      matchConfig.Type = "ether";
      networkConfig = {
        DHCP = "yes";
        IPv6AcceptRA = true;
      };
    };
  };

  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "no";
      PasswordAuthentication = true;
    };
  };
}
