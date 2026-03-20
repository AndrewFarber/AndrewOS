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
  bootloaders.systemd.enable = true;

}
