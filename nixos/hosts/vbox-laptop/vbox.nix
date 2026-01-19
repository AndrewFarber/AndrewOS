{ ... }:

{
  virtualisation.virtualbox.guest.enable = true;

  # VirtualBox lacks GPU acceleration for wlroots-based compositors (Sway).
  # Force software rendering to fix greetd/sway render errors.
  environment.sessionVariables = {
    WLR_RENDERER = "pixman";
    WLR_NO_HARDWARE_CURSORS = "1";
  };
}
