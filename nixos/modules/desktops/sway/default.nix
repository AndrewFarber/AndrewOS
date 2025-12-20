# =============================================================================
# AndrewOS Sway Desktop Module
# =============================================================================
#
# This module configures a complete Sway desktop environment for Wayland.
# Sway is a tiling window manager and a drop-in replacement for i3, but for
# Wayland instead of X11.
#
# Components installed:
#   - Sway:        Tiling Wayland compositor (window manager)
#   - Waybar:      Highly customizable status bar
#   - Fuzzel:      Fast, lightweight application launcher
#   - Mako:        Lightweight notification daemon
#   - Swaylock:    Screen locker
#   - Swayidle:    Idle management daemon (auto-lock, suspend)
#   - Grim/Slurp:  Screenshot tools
#   - PipeWire:    Modern audio/video server (replaces PulseAudio)
#   - Greetd:      Minimal login manager with TUI greeter
#
# User configuration files:
#   - ~/.config/sway/config      - Sway keybindings and appearance
#   - ~/.config/waybar/config    - Status bar modules
#   - ~/.config/waybar/style.css - Status bar styling
#
# These dotfiles are managed in home-manager and only loaded when
# desktop = "sway" is set in flake.nix.
#
# Usage:
#   In flake.nix, set: desktop = "sway";
#   Then run: sudo nixos-rebuild switch --flake .#<host>
#
# =============================================================================

{ pkgs, ... }:

{
  # ===========================================================================
  # Sway Window Manager
  # ===========================================================================
  # Sway is a Wayland compositor that implements the i3 window manager's
  # features. It provides tiling window management, workspaces, and extensive
  # keyboard-driven control.
  #
  # wrapperFeatures.gtk: Enables GTK integration for proper theming of GTK
  # applications running under Sway.

  programs.sway = {
    enable = true;
    wrapperFeatures.gtk = true;

    # Extra packages installed alongside Sway
    extraPackages = with pkgs; [
      # -----------------------------------------------------------------------
      # Status Bar
      # -----------------------------------------------------------------------
      # Waybar: Highly customizable Wayland bar with modules for system info,
      # workspaces, tray, and more. Configured via ~/.config/waybar/
      waybar

      # -----------------------------------------------------------------------
      # Application Launcher
      # -----------------------------------------------------------------------
      # Fuzzel: Fast, minimalist application launcher for Wayland.
      # Triggered with $mod+d in sway config.
      fuzzel

      # -----------------------------------------------------------------------
      # Notifications
      # -----------------------------------------------------------------------
      # Mako: Lightweight notification daemon designed for Sway/Wayland.
      # libnotify: Provides notify-send command for sending notifications.
      mako
      libnotify

      # -----------------------------------------------------------------------
      # Screen Lock & Idle Management
      # -----------------------------------------------------------------------
      # Swaylock: Screen locker that integrates with Sway.
      # Swayidle: Daemon that monitors idle time and triggers actions
      #           (lock screen after 5min, turn off display after 10min).
      swaylock
      swayidle

      # -----------------------------------------------------------------------
      # Screenshot Tools
      # -----------------------------------------------------------------------
      # Grim: Grab images from Wayland compositor (screenshot tool).
      # Slurp: Select a region in a Wayland compositor (for partial screenshots).
      # Usage: grim -g "$(slurp)" - | wl-copy  (screenshot region to clipboard)
      grim
      slurp

      # -----------------------------------------------------------------------
      # Clipboard
      # -----------------------------------------------------------------------
      # wl-clipboard: Command-line copy/paste utilities for Wayland.
      # Provides wl-copy and wl-paste commands.
      wl-clipboard

      # -----------------------------------------------------------------------
      # Hardware Controls
      # -----------------------------------------------------------------------
      # Brightnessctl: Control device brightness (laptop screens, keyboards).
      # Used by media key bindings in sway config.
      brightnessctl

      # Pavucontrol: GTK volume control for PulseAudio/PipeWire.
      # Launched by clicking the audio module in waybar.
      pavucontrol
    ];
  };

  # ===========================================================================
  # XWayland Compatibility Layer
  # ===========================================================================
  # XWayland provides backward compatibility for X11 applications that don't
  # yet support Wayland natively. Most modern apps work fine, but some older
  # applications or games may require XWayland.

  programs.xwayland.enable = true;

  # ===========================================================================
  # Display Manager (Login Screen)
  # ===========================================================================
  # Greetd is a minimal login manager that works well with Wayland compositors.
  # Tuigreet provides a simple terminal-based login interface.

  services.greetd = {
    enable = true;
    settings = {
      default_session = {
        command = "${pkgs.tuigreet}/bin/tuigreet --time --cmd sway";
        user = "greeter";
      };
    };
  };

  # ===========================================================================
  # Audio Stack (PipeWire)
  # ===========================================================================
  # PipeWire is a modern multimedia framework that replaces PulseAudio and
  # JACK. It provides lower latency, better Bluetooth audio, and native
  # Wayland screen sharing support.
  #
  # rtkit: Allows PipeWire to acquire realtime scheduling for low-latency audio.
  # alsa: ALSA compatibility layer for applications using ALSA directly.
  # pulse: PulseAudio compatibility layer for applications using PulseAudio API.

  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;  # For 32-bit applications (games, Wine)
    pulse.enable = true;        # PulseAudio compatibility
  };

  # ===========================================================================
  # Keyboard Configuration
  # ===========================================================================
  # Configure keyboard layout and options. These settings apply system-wide
  # and are also inherited by the console (TTY).
  #
  # ctrl:nocaps: Remap Caps Lock to Ctrl (useful for Vim/Emacs users).
  # This matches the setting in other desktop modules (GNOME, Plasma).

  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };
  console.useXkbConfig = true;  # Apply same keyboard config to TTY console
  services.xserver.xkb.options = "ctrl:nocaps";

  # ===========================================================================
  # Polkit (Authentication Agent)
  # ===========================================================================
  # Polkit handles authorization for privileged operations. When an application
  # needs elevated permissions (e.g., installing software, mounting drives),
  # polkit shows an authentication dialog.
  #
  # Note: You may want to add a graphical polkit agent like lxqt-policykit
  # to extraPackages if you need GUI authentication prompts.

  security.polkit.enable = true;

  # ===========================================================================
  # DConf (GTK Settings Database)
  # ===========================================================================
  # DConf is the configuration system used by GTK applications and GNOME.
  # Enabling it allows GTK apps to properly store and retrieve their settings.

  programs.dconf.enable = true;

  # ===========================================================================
  # XDG Desktop Portal
  # ===========================================================================
  # XDG portals provide a standardized way for sandboxed applications to
  # interact with the desktop. Required for:
  #   - File chooser dialogs (in sandboxed apps like Firefox, Flatpaks)
  #   - Screen sharing (for video calls, OBS, etc.)
  #   - Opening URLs in default browser
  #
  # wlr: Portal backend specifically for wlroots-based compositors like Sway.
  # gtk: GTK portal for file dialogs and other GTK-specific features.

  xdg.portal = {
    enable = true;
    wlr.enable = true;  # wlroots-specific portal (screen sharing for Sway)
    extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
  };

  # ===========================================================================
  # Fonts
  # ===========================================================================
  # Essential fonts for a complete desktop experience:
  #   - Noto: Google's font family with broad Unicode coverage
  #   - Noto CJK: Chinese, Japanese, Korean character support
  #   - Noto Emoji: Color emoji support
  #   - Font Awesome: Icon font used by waybar for system icons
  #
  # Note: The waybar config expects "MesloLGS Nerd Font" which should be
  # installed separately if you want the full icon experience.

  fonts.packages = with pkgs; [
    noto-fonts
    noto-fonts-cjk-sans
    noto-fonts-color-emoji
    font-awesome
  ];
}
