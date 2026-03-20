{ host, desktop, inputs, ... }:

{
  imports = [
    ./hardware.nix
    ./vbox.nix
    ../../modules/bootloaders
    ../../modules/desktops
    ../../modules/networking
    ../../modules/core
  ];

  # Boot Loader
  andrewos.bootloader.systemd.enable = true;

}
