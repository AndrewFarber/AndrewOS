{ pkgs, ... }:

let
  mkScript = name: { runtimeInputs ? [], file }:
    pkgs.writeShellApplication {
      inherit name runtimeInputs;
      text = builtins.readFile file;
    };
in {
  home.packages = [
    (mkScript "andrewos-gc" { file = ../bin/andrewos-gc; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "andrewos-gc-system" { file = ../bin/andrewos-gc-system; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "andrewos-launch-audio" { file = ../bin/andrewos-launch-audio; runtimeInputs = [ pkgs.alacritty pkgs.pulsemixer ]; })
    (mkScript "andrewos-launch-bluetooth" { file = ../bin/andrewos-launch-bluetooth; runtimeInputs = [ pkgs.alacritty pkgs.bluetuith ]; })
    (mkScript "andrewos-launch-browser" { file = ../bin/andrewos-launch-browser; runtimeInputs = [ pkgs.chromium ]; })
    (mkScript "andrewos-launch-disk" { file = ../bin/andrewos-launch-disk; runtimeInputs = [ pkgs.alacritty ]; })
    (mkScript "andrewos-launch-docker" { file = ../bin/andrewos-launch-docker; runtimeInputs = [ pkgs.alacritty pkgs.lazydocker ]; })
    (mkScript "andrewos-launch-editor" { file = ../bin/andrewos-launch-editor; runtimeInputs = [ pkgs.alacritty pkgs.neovim ]; })
    (mkScript "andrewos-launch-files" { file = ../bin/andrewos-launch-files; runtimeInputs = [ pkgs.alacritty pkgs.yazi ]; })
    (mkScript "andrewos-launch-git" { file = ../bin/andrewos-launch-git; runtimeInputs = [ pkgs.alacritty pkgs.lazygit ]; })
    (mkScript "andrewos-launch-monitor" { file = ../bin/andrewos-launch-monitor; runtimeInputs = [ pkgs.alacritty pkgs.btop ]; })
    (mkScript "andrewos-launch-network" { file = ../bin/andrewos-launch-network; runtimeInputs = [ pkgs.alacritty pkgs.impala ]; })
    (mkScript "andrewos-launch-terminal" { file = ../bin/andrewos-launch-terminal; runtimeInputs = [ pkgs.alacritty ]; })
    (mkScript "andrewos-menu" { file = ../bin/andrewos-menu; runtimeInputs = [ pkgs.fuzzel ]; })
    (mkScript "andrewos-move-workspace" { file = ../bin/andrewos-move-workspace; runtimeInputs = [ pkgs.fuzzel pkgs.sway pkgs.jq ]; })
    (mkScript "andrewos-rename-workspace" { file = ../bin/andrewos-rename-workspace; runtimeInputs = [ pkgs.fuzzel pkgs.sway pkgs.jq ]; })
    (mkScript "andrewos-rebuild" { file = ../bin/andrewos-rebuild; runtimeInputs = [ pkgs.alacritty ]; })
    (mkScript "andrewos-resolution" { file = ../bin/andrewos-resolution; runtimeInputs = [ pkgs.fuzzel pkgs.wlr-randr ]; })
    (mkScript "andrewos-refresh-swaync" { file = ../bin/andrewos-refresh-swaync; runtimeInputs = [ pkgs.swaynotificationcenter ]; })
    (mkScript "andrewos-refresh-tmux" { file = ../bin/andrewos-refresh-tmux; runtimeInputs = [ pkgs.tmux ]; })
    (mkScript "andrewos-refresh-waybar" { file = ../bin/andrewos-refresh-waybar; })
    (mkScript "andrewos-refresh-wm" { file = ../bin/andrewos-refresh-wm; runtimeInputs = [ pkgs.sway ]; })
    (mkScript "andrewos-restart-pipewire" { file = ../bin/andrewos-restart-pipewire; })
    (mkScript "andrewos-rotate" { file = ../bin/andrewos-rotate; runtimeInputs = [ pkgs.fuzzel pkgs.wlr-randr ]; })
    (mkScript "andrewos-scale" { file = ../bin/andrewos-scale; runtimeInputs = [ pkgs.fuzzel pkgs.wlr-randr ]; })
    (mkScript "andrewos-restart-wifi" { file = ../bin/andrewos-restart-wifi; })
    (mkScript "andrewos-screenshot-area" { file = ../bin/andrewos-screenshot-area; runtimeInputs = [ pkgs.grim pkgs.slurp pkgs.wl-clipboard ]; })
    (mkScript "andrewos-screenshot-save" { file = ../bin/andrewos-screenshot-save; runtimeInputs = [ pkgs.grim pkgs.slurp ]; })
    (mkScript "andrewos-screenshot-screen" { file = ../bin/andrewos-screenshot-screen; runtimeInputs = [ pkgs.grim pkgs.wl-clipboard ]; })
    (mkScript "andrewos-shortcuts" { file = ../bin/andrewos-shortcuts; runtimeInputs = [ pkgs.fuzzel ]; })
    (mkScript "andrewos-theme" { file = ../bin/andrewos-theme; runtimeInputs = [ pkgs.alacritty pkgs.fuzzel pkgs.gnused pkgs.swaynotificationcenter pkgs.swaybg ]; })
    (mkScript "andrewos-toggle-bluetooth" { file = ../bin/andrewos-toggle-bluetooth; runtimeInputs = [ pkgs.bluez ]; })
    (mkScript "andrewos-toggle-display" { file = ../bin/andrewos-toggle-display; runtimeInputs = [ pkgs.fuzzel pkgs.wlr-randr ]; })
    (mkScript "andrewos-toggle-nightlight" { file = ../bin/andrewos-toggle-nightlight; runtimeInputs = [ pkgs.wlsunset pkgs.procps ]; })
    (mkScript "andrewos-toggle-wifi" { file = ../bin/andrewos-toggle-wifi; runtimeInputs = [ pkgs.util-linux ]; })
    (mkScript "andrewos-update" { file = ../bin/andrewos-update; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "andrewos-wallpaper" { file = ../bin/andrewos-wallpaper; runtimeInputs = [ pkgs.fuzzel pkgs.sway ]; })
    (mkScript "andrewos-workspace-wrap" { file = ../bin/andrewos-workspace-wrap; runtimeInputs = [ pkgs.sway pkgs.jq ]; })
  ];
}
