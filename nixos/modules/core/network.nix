{ host, ... }:

{
  networking.hostName = host;
  networking.firewall.enable = true;
}
