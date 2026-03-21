{ userConfig, ... }:

{
  nix = {
    settings = {
      download-buffer-size = 250000000;
      auto-optimise-store = true;
      experimental-features = [ "nix-command" "flakes" ];
    };
  };
  time.timeZone = userConfig.timezone;
  i18n.defaultLocale = "en_US.UTF-8";
  system.stateVersion = "24.11"; # Do not change!!
}
