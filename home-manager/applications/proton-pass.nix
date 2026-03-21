{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.proton-pass.enable = lib.mkEnableOption "Proton Pass";

  config = lib.mkIf config.andrewos.applications.proton-pass.enable {
    xdg.desktopEntries.proton-pass = {
      name = "Proton Pass";
      comment = "Proton Pass password manager";
      exec = "${pkgs.chromium}/bin/chromium --app=https://account.proton.me/pass";
      icon = "${../../assets/icons/proton-pass.png}";
      terminal = false;
      categories = [ "Network" ];
    };
  };
}
