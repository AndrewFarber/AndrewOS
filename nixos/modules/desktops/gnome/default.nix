{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    xclip
  ];

  services.xserver.enable = true;
  services.xserver.displayManager.gdm.enable = true;
  services.xserver.desktopManager.gnome.enable = true;
  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  console.useXkbConfig = true;

  # If the below Caps Lock to Ctrl remap is not working, run the below then reboot
  # gsettings reset org.gnome.desktop.input-sources xkb-options
  # gsettings reset org.gnome.desktop.input-sources sources
  services.xserver.xkb.options = "ctrl:nocaps";

}

