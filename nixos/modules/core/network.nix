{ host, ... }:

{
  networking.hostName = host;
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
