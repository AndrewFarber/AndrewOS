{ host, desktop, inputs, ... }:

{
  imports = [
    ./hardware.nix
    ./vbox.nix
    ../../modules/bootloaders
    ../../modules/desktops
    ../../modules/core
  ];

  # Boot Loader
  bootloaders.systemd.enable = true;

}
