{ desktop ? "", pkgs, ... }:

let
  wmPrefix = "sway";
in

{
  programs.waybar = {
    enable = true;
    systemd.enable = true;
    settings = {
      mainBar = {
        layer = "top";
        position = "top";
        height = 30;
        spacing = 8;

        modules-left = [ "${wmPrefix}/workspaces" "${wmPrefix}/mode" ];
        modules-center = [ "${wmPrefix}/window" ];
        modules-right = [ "network" "bluetooth" "pulseaudio" "cpu" "memory" "disk" "battery" "clock" "custom/notification" "tray" ];

        "${wmPrefix}/workspaces" = {
          disable-scroll = true;
          all-outputs = true;
          format = "{name}";
        };

        "${wmPrefix}/mode" = {
          format = "<span style=\"italic\">{}</span>";
        };

        "${wmPrefix}/window" = {
          max-length = 50;
        };

        tray = {
          spacing = 10;
        };

        clock = {
          format = "󰥔 {:%H:%M}";
          format-alt = "󰥔 {:%Y-%m-%d %H:%M}";
          tooltip-format = "<tt>{calendar}</tt>";
        };

        cpu = {
          format = "󰍛 {usage}%";
          tooltip = true;
          on-click = "andrewos-launch-monitor";
        };

        memory = {
          format = "󰘚 {}%";
          on-click = "andrewos-launch-monitor";
        };

        disk = {
          format = "󰋊 {percentage_used}%";
          path = "/";
          interval = 30;
          tooltip-format = "{used} / {total} used on {path}";
          on-click = "andrewos-launch-monitor";
        };

        battery = {
          format = "{icon} {capacity}%";
          format-charging = "󰂄 {capacity}%";
          format-plugged = "󰚥 {capacity}%";
          format-icons = [ "󰁺" "󰁻" "󰁼" "󰁽" "󰁾" "󰁿" "󰂀" "󰂁" "󰂂" "󰁹" ];
          states = {
            warning = 30;
            critical = 15;
          };
          tooltip-format = "{timeTo} — {capacity}%";
        };

        network = {
          format-wifi = "󰤨 {signalStrength}%";
          format-ethernet = "󰈀";
          format-disconnected = "󰤭";
          tooltip-format-wifi = "{essid} ({signalStrength}%)";
          tooltip-format-ethernet = "{ifname}: {ipaddr}";
          tooltip-format-disconnected = "Disconnected";
          on-click = "andrewos-launch-network";
        };

        bluetooth = {
          format = "󰂯";
          format-connected = "󰂱 {num_connections}";
          format-disabled = "󰂲";
          tooltip-format = "{controller_alias}\n{num_connections} connected";
          tooltip-format-connected = "{controller_alias}\n{num_connections} connected\n\n{device_enumerate}";
          tooltip-format-enumerate-connected = "{device_alias}";
          on-click = "andrewos-launch-bluetooth";
        };

        "custom/notification" = {
          tooltip = false;
          format = "{icon}";
          format-icons = {
            notification = "󱅫";
            none = "󰂚";
            dnd-notification = "󰂛";
            dnd-none = "󰂛";
          };
          return-type = "json";
          exec = "${pkgs.swaynotificationcenter}/bin/swaync-client -swb";
          on-click = "${pkgs.swaynotificationcenter}/bin/swaync-client -t -sw";
          on-click-right = "${pkgs.swaynotificationcenter}/bin/swaync-client -d -sw";
          escape = true;
        };

        pulseaudio = {
          format = "{icon} {volume}%";
          format-muted = "󰝟";
          format-icons = {
            default = [ "󰕿" "󰖀" "󰕾" ];
            headphone = "󰋋";
          };
          tooltip-format = "{desc} — {volume}%";
          on-click = "andrewos-launch-audio";
        };
      };
    };
  };
}
