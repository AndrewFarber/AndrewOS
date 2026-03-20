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
  andrewos.bootloader.systemd.enable = true;

  # Wireless
  andrewos.networking.wireless.enable = true;

  # Bluetooth
  andrewos.networking.bluetooth.enable = true;

}
