{ host, desktop, inputs, ... }:

{
  imports = [
    ./hardware.nix
    ../../modules/bootloaders
    ../../modules/desktops
    ../../modules/drivers
    ../../modules/core
  ];

  # Boot Loader
  bootloaders.systemd.enable = true;

  # GPU Driver
  drivers.vbox.enable = true;

}
