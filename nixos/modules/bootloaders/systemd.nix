{ lib, config, ... }:

with lib;
let
  cfg = config.bootloaders.systemd;
in {

  options.bootloaders.systemd = {
    enable = mkEnableOption "Enable Systemd";
  };

  config = mkIf cfg.enable {
    boot.loader.systemd-boot.enable = true;
    boot.loader.efi.canTouchEfiVariables = true;
  };

}
