{ config, pkgs, ... }:

{

  programs.sway = {
    enable = true;
    wrapperFeatures.gtk = true;

    extraPackages = with pkgs; [
      waybar
      fuzzel
      mako
      libnotify
      swaylock
      swayidle
      grim
      slurp
      wl-clipboard
      pavucontrol
    ];
  };

  programs.xwayland.enable = true;

  services.greetd = {
    enable = true;
    settings = {
      default_session = {
        command = "${pkgs.greetd.tuigreet}/bin/tuigreet --time --sessions ${config.services.displayManager.sessionData.desktops}/share/wayland-sessions";
        user = "greeter";
      };
    };
  };

  # Prevent kernel messages from overwriting tuigreet
  boot.kernelParams = [ "console=tty1" ];
  systemd.services.greetd.serviceConfig = {
    Type = "idle";
    StandardInput = "tty";
    StandardOutput = "tty";
    StandardError = "journal";
    TTYReset = true;
    TTYVHangup = true;
    TTYVTDisallocate = true;
  };

  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;  # For 32-bit applications (games, Wine)
    pulse.enable = true;        # PulseAudio compatibility
  };

  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  console.useXkbConfig = true;  # Apply same keyboard config to TTY console
  services.xserver.xkb.options = "ctrl:nocaps";

  security.polkit.enable = true;

  programs.dconf.enable = true;

  xdg.portal = {
    enable = true;
    wlr.enable = true;  # wlroots-specific portal (screen sharing for Sway)
    extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
  };

  fonts.packages = with pkgs; [
    noto-fonts
    noto-fonts-cjk-sans
    noto-fonts-color-emoji
    font-awesome
  ];
}
