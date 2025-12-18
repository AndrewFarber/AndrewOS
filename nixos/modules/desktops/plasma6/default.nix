{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    wl-clipboard
  ];

  services.xserver.enable = true;
  services.displayManager.sddm.enable = true;
  services.displayManager.sddm.wayland.enable = true;
  services.desktopManager.plasma6.enable = true;
  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  console.useXkbConfig = true;

  # If the below Caps Lock to Ctrl remap is not working, run the below then reboot
  # gsettings reset org.gnome.desktop.input-sources xkb-options
  # gsettings reset org.gnome.desktop.input-sources sources
  services.xserver.xkb.options = "ctrl:nocaps";

  environment.plasma6.excludePackages = with pkgs.kdePackages; [
    elisa
    gwenview
    kate
    okular
  ];

}

