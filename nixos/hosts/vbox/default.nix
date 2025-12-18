{ host, desktop, inputs, username, ... }:

{
  imports = [
    ./hardware.nix
    ../../modules/bootloaders
    ../../modules/desktops
    ../../modules/drivers
    ../../modules/core
  ];

  # Boot Loaders
  bootloaders.grub.enable = false;
  bootloaders.systemd.enable = true;

  # GPU Drivers
  drivers.vbox.enable = true;
  drivers.nvidia.enable = false;

}
