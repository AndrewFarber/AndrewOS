{ host, ... }:

{
  networking.hostName = host;
  networking.firewall.enable = true;
  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "no";
      PasswordAuthentication = true;
    };
  };
}
