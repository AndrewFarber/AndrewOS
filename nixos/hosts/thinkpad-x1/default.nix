{ host, desktop, inputs, ... }:

{
  imports = [
    ./hardware.nix
    ../../modules/bootloaders
    ../../modules/desktops
    ../../modules/networking
    ../../modules/core
  ];

  # Boot Loader
  bootloaders.systemd.enable = true;

  # Wireless
  networking-modules.wireless.enable = true;

}
