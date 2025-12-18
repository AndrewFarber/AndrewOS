{ lib, config, ... }:

with lib;
let
  cfg = config.drivers.vbox;
in {
  options.drivers.vbox = {
    enable = mkEnableOption "Enable VM Guest Services";
  };

  config = mkIf cfg.enable {
    virtualisation.virtualbox.guest.enable = true;
  };

}
