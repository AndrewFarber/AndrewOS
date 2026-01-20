{ config, pkgs, ... }:

{
  programs.hyprland = {
    enable = true;
    xwayland.enable = true;
  };

  services.greetd = {
    enable = true;
    settings = {
      default_session = {
        command = "${pkgs.tuigreet}/bin/tuigreet --time --sessions ${config.services.displayManager.sessionData.desktops}/share/wayland-sessions";
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
    alsa.support32Bit = true;
    pulse.enable = true;
  };

  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  console.useXkbConfig = true;
  services.xserver.xkb.options = "ctrl:nocaps";

  security.polkit.enable = true;

  programs.dconf.enable = true;

  xdg.portal = {
    enable = true;
    extraPortals = [ pkgs.xdg-desktop-portal-gtk ];  # GTK fallback for file pickers
  };

  environment.systemPackages = with pkgs; [
    waybar
    fuzzel
    mako
    libnotify
    hyprlock
    hypridle
    hyprpolkitagent
    grim
    slurp
    wl-clipboard
    pavucontrol
    qt6.qtwayland
    swaybg
    kitty
  ];

  environment.sessionVariables = {
    QT_QPA_PLATFORM = "wayland";
    QT_WAYLAND_DISABLE_WINDOWDECORATION = "1";
  };

  fonts.packages = with pkgs; [
    noto-fonts
    noto-fonts-cjk-sans
    noto-fonts-color-emoji
    font-awesome
    nerd-fonts.meslo-lg
  ];
}
