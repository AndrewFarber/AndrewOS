{ desktop, ... }:

{
  virtualisation.virtualbox.guest.enable = true;

  # Blacklist vmwgfx (VMware SVGA driver) — it loads by default because
  # VirtualBox emulates a VMware SVGA adapter, but it is the wrong driver
  # and produces "unsupported hypervisor" and "Failed to open channel" errors.
  # The VirtualBox guest additions provide the correct vboxvideo driver.
  boot.blacklistedKernelModules = [ "vmwgfx" ];

  # Disable VBoxClient services that do not work on Wayland/XWayland
  # and restart-loop indefinitely, wasting resources.
  systemd.user.services.virtualboxClientDragAndDrop.enable = false;
  systemd.user.services.virtualboxClientVmsvga.enable = false;

  # VirtualBox environment variables for Wayland compositors.
  # Sway supports pixman software rendering, but Hyprland requires OpenGL.
  # For Hyprland, enable 3D Acceleration in VirtualBox VM settings.
  environment.sessionVariables = {
    WLR_NO_HARDWARE_CURSORS = "1";
  } // (if desktop == "sway" then {
    WLR_RENDERER = "pixman";
  } else {});
}
