{ pkgs, ... }:

let
  config = builtins.toJSON {
    "$schema" = "/etc/xdg/swaync/configSchema.json";
    positionX = "right";
    positionY = "top";
    layer = "overlay";
    control-center-layer = "top";
    layer-shell = true;
    cssPriority = "application";
    control-center-margin-top = 8;
    control-center-margin-bottom = 8;
    control-center-margin-right = 8;
    control-center-width = 400;
    notification-icon-size = 48;
    notification-body-image-height = 100;
    notification-body-image-width = 200;
    timeout = 6;
    timeout-low = 4;
    timeout-critical = 0;
    fit-to-screen = true;
    notification-window-width = 400;
    keyboard-shortcuts = true;
    image-visibility = "when-available";
    transition-time = 200;
    hide-on-clear = false;
    hide-on-action = true;
    script-fail-notify = true;

    widgets = [
      "title"
      "buttons-grid"
      "menubar"
      "mpris"
      "volume"
      "backlight"
      "dnd"
      "notifications"
    ];

    widget-config = {
      title = {
        text = "Notifications";
        clear-all-button = true;
        button-text = "Clear All";
      };
      dnd = {
        text = "Do Not Disturb";
      };
      buttons-grid = {
        actions = [
          {
            label = "󰤨";
            type = "toggle";
            active = true;
            command = "toggle-wifi";
            update-command = "toggle-wifi check";
          }
          {
            label = "󰂯";
            type = "toggle";
            active = true;
            command = "toggle-bluetooth";
            update-command = "toggle-bluetooth check";
          }
          {
            label = "󰌶";
            type = "toggle";
            active = false;
            command = "toggle-nightlight";
            update-command = "toggle-nightlight check";
          }
        ];
      };
      menubar = {
        "menu#power" = {
          label = "⏻ Power";
          position = "left";
          animation-type = "slide_down";
          animation-duration = 250;
          actions = [
            { label = "󰌾 Lock"; command = "swaylock -f"; }
            { label = "󰤄 Suspend"; command = "systemctl suspend"; }
            { label = "󰜉 Reboot"; command = "systemctl reboot"; }
            { label = "󰐥 Shutdown"; command = "systemctl poweroff"; }
          ];
        };
        "menu#system" = {
          label = " System";
          position = "right";
          animation-type = "slide_down";
          animation-duration = 250;
          actions = [
            { label = "󰍹 System Monitor"; command = "launch-monitor"; }
            { label = "󰋊 Disk Usage"; command = "launch-disk"; }
            { label = " Audio Settings"; command = "launch-audio"; }
            { label = "󰂯 Bluetooth"; command = "launch-bluetooth"; }
          ];
        };
      };
      mpris = {
        show-album-art = "when-available";
        autohide = true;
      };
      volume = {
        label = "󰕾";
        show-per-app = false;
      };
      backlight = {
        label = "󰃟";
        device = "intel_backlight";
        subsystem = "backlight";
        min = 0;
      };
    };
  };
in
{
  home.file.".config/swaync/config.json".text = config;
}
