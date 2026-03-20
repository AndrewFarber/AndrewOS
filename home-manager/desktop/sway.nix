{ pkgs, lib, theme, ... }:

{
  wayland.windowManager.sway = {
    enable = true;
    config = {
      modifier = "Mod4";
      terminal = "alacritty";
      menu = "fuzzel";

      left = "h";
      down = "j";
      up = "k";
      right = "l";

      input = {
        "type:keyboard" = {
          xkb_options = "ctrl:nocaps";
        };
        "type:touchpad" = {
          tap = "enabled";
          natural_scroll = "enabled";
        };
      };

      keybindings = let
        mod = "Mod4";
      in {
        "${mod}+Return" = "exec alacritty";
        "${mod}+Shift+q" = "kill";
        "${mod}+d" = "exec menu";
        "${mod}+Shift+c" = "reload";
        "${mod}+Escape" = "exec swaylock -f -c ${theme.lockColor}";
        "${mod}+Shift+s" = ''exec grim -g "$(slurp)" - | wl-copy'';

        "${mod}+h" = "focus left";
        "${mod}+j" = "focus down";
        "${mod}+k" = "focus up";
        "${mod}+l" = "focus right";

        "${mod}+Shift+h" = "move left";
        "${mod}+Shift+j" = "move down";
        "${mod}+Shift+k" = "move up";
        "${mod}+Shift+l" = "move right";

        "${mod}+1" = "workspace number 1";
        "${mod}+2" = "workspace number 2";
        "${mod}+3" = "workspace number 3";
        "${mod}+4" = "workspace number 4";
        "${mod}+5" = "workspace number 5";
        "${mod}+6" = "workspace number 6";
        "${mod}+7" = "workspace number 7";
        "${mod}+8" = "workspace number 8";
        "${mod}+9" = "workspace number 9";
        "${mod}+0" = "workspace number 10";

        "${mod}+Shift+1" = "move container to workspace number 1";
        "${mod}+Shift+2" = "move container to workspace number 2";
        "${mod}+Shift+3" = "move container to workspace number 3";
        "${mod}+Shift+4" = "move container to workspace number 4";
        "${mod}+Shift+5" = "move container to workspace number 5";
        "${mod}+Shift+6" = "move container to workspace number 6";
        "${mod}+Shift+7" = "move container to workspace number 7";
        "${mod}+Shift+8" = "move container to workspace number 8";
        "${mod}+Shift+9" = "move container to workspace number 9";
        "${mod}+Shift+0" = "move container to workspace number 10";

        "${mod}+b" = "splith";
        "${mod}+v" = "splitv";

        "${mod}+space" = "exec fuzzel";
        "${mod}+Alt+v" = ''exec cliphist list | fuzzel --dmenu | cliphist decode | wl-copy'';
        "${mod}+Alt+w" = "exec wallpaper";
        "${mod}+Shift+minus" = "move scratchpad";
        "${mod}+minus" = "scratchpad show";

        "${mod}+Shift+slash" = "exec shortcuts";
        "${mod}+Shift+e" = "exec wlogout";

        # Volume (pamixer)
        "XF86AudioRaiseVolume" = "exec pamixer -i 5";
        "XF86AudioLowerVolume" = "exec pamixer -d 5";
        "XF86AudioMute" = "exec pamixer -t";

        # Brightness (brightnessctl)
        "XF86MonBrightnessUp" = "exec brightnessctl set +5%";
        "XF86MonBrightnessDown" = "exec brightnessctl set 5%-";

        # Media (playerctl)
        "XF86AudioPlay" = "exec playerctl play-pause";
        "XF86AudioNext" = "exec playerctl next";
        "XF86AudioPrev" = "exec playerctl previous";

        "${mod}+r" = "mode resize";
      };

      modes = {
        resize = {
          "h" = "resize shrink width 10px";
          "j" = "resize grow height 10px";
          "k" = "resize shrink height 10px";
          "l" = "resize grow width 10px";
          "Left" = "resize shrink width 10px";
          "Down" = "resize grow height 10px";
          "Up" = "resize shrink height 10px";
          "Right" = "resize grow width 10px";
          "Return" = "mode default";
          "Escape" = "mode default";
        };
      };

      window = {
        titlebar = false;
        border = 2;
        commands = [
          { command = "floating enable, resize set 80 ppt 70 ppt"; criteria = { app_id = "floating-term"; }; }
          { command = "floating enable, resize set 80 ppt 70 ppt"; criteria = { title = "File Manager"; }; }
        ];
      };

      floating = {
        border = 2;
      };

      gaps = {
        inner = 8;
        outer = 4;
      };

      bars = [];

      startup = [
        { command = "wl-paste --watch cliphist store"; }
        { command = "swaync"; }
        { command = "sway-audio-idle-inhibit"; }
        { command = "swayidle -w timeout 300 'swaylock -f -c ${theme.lockColor}' timeout 600 'systemctl suspend' before-sleep 'swaylock -f -c ${theme.lockColor}'"; }
      ];
    };

    extraConfig = ''
      include ~/.config/sway/theme
      include /etc/sway/config.d/*
      workspace 1
    '';
  };
}
