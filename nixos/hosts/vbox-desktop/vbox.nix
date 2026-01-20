{ desktop, ... }:

{
  virtualisation.virtualbox.guest.enable = true;

  # VirtualBox environment variables for Wayland compositors.
  # Sway supports pixman software rendering, but Hyprland requires OpenGL.
  # For Hyprland, enable 3D Acceleration in VirtualBox VM settings.
  environment.sessionVariables = {
    WLR_NO_HARDWARE_CURSORS = "1";
  } // (if desktop == "sway" then {
    WLR_RENDERER = "pixman";
  } else {});
}
