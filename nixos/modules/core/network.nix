{ host, ... }:

{
  networking.hostName = host;
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
