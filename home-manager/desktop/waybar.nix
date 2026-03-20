{ desktop ? "", ... }:

let
  wmPrefix = if desktop == "hyprland" then "hyprland" else "sway";
in

{
  programs.waybar = {
    enable = true;
    systemd.enable = false;
    settings = {
      mainBar = {
        layer = "top";
        position = "top";
        height = 30;
        spacing = 8;

        modules-left = [ "${wmPrefix}/workspaces" "${wmPrefix}/mode" ];
        modules-center = [ "${wmPrefix}/window" ];
        modules-right = [ "cpu" "memory" "clock" "tray" ];

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
          format = "{:%H:%M}";
          format-alt = "{:%Y-%m-%d %H:%M}";
          tooltip-format = "<tt>{calendar}</tt>";
        };

        cpu = {
          format = " {usage}%";
          tooltip = true;
        };

        memory = {
          format = " {}%";
        };
      };
    };
  };
}
