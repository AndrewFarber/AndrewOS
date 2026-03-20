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
  # Sway uses pixman software rendering (no GPU acceleration needed).
  environment.sessionVariables = {
    WLR_NO_HARDWARE_CURSORS = "1";
    WLR_RENDERER = "pixman";
  };
}
