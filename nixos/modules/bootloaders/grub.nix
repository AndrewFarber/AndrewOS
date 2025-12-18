{ lib, config, ... }:

with lib;
let
  cfg = config.bootloaders.grub;
in {

  options.bootloaders.grub = {
    enable = mkEnableOption "Enable Grub";
  };

  config = mkIf cfg.enable {
    boot.loader.grub.enable = true;
    boot.loader.grub.device = "/dev/sda";
    boot.loader.grub.useOSProber = true;
  };

}
