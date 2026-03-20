{ pkgs, ... }:

let
  mkScript = name: { runtimeInputs ? [], file }:
    pkgs.writeShellApplication {
      inherit name runtimeInputs;
      text = builtins.readFile file;
    };
in {
  home.packages = [
    (mkScript "gc" { file = ../bin/gc; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "gc-system" { file = ../bin/gc-system; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "launch-audio" { file = ../bin/launch-audio; runtimeInputs = [ pkgs.pavucontrol ]; })
    (mkScript "launch-browser" { file = ../bin/launch-browser; runtimeInputs = [ pkgs.chromium ]; })
    (mkScript "launch-docker" { file = ../bin/launch-docker; runtimeInputs = [ pkgs.alacritty pkgs.lazydocker ]; })
    (mkScript "launch-editor" { file = ../bin/launch-editor; runtimeInputs = [ pkgs.alacritty pkgs.neovim ]; })
    (mkScript "launch-files" { file = ../bin/launch-files; runtimeInputs = [ pkgs.alacritty pkgs.yazi ]; })
    (mkScript "launch-git" { file = ../bin/launch-git; runtimeInputs = [ pkgs.alacritty pkgs.lazygit ]; })
    (mkScript "launch-terminal" { file = ../bin/launch-terminal; runtimeInputs = [ pkgs.alacritty ]; })
    (mkScript "lock" { file = ../bin/lock; runtimeInputs = [ pkgs.swaylock pkgs.hyprlock ]; })
    (mkScript "menu" { file = ../bin/menu; runtimeInputs = [ pkgs.fuzzel ]; })
    (mkScript "rebuild" { file = ../bin/rebuild; runtimeInputs = [ pkgs.alacritty ]; })
    (mkScript "refresh-mako" { file = ../bin/refresh-mako; runtimeInputs = [ pkgs.mako ]; })
    (mkScript "refresh-tmux" { file = ../bin/refresh-tmux; runtimeInputs = [ pkgs.tmux ]; })
    (mkScript "refresh-waybar" { file = ../bin/refresh-waybar; runtimeInputs = [ pkgs.waybar ]; })
    (mkScript "refresh-wm" { file = ../bin/refresh-wm; runtimeInputs = [ pkgs.sway ]; })
    (mkScript "restart-mako" { file = ../bin/restart-mako; runtimeInputs = [ pkgs.mako ]; })
    (mkScript "restart-pipewire" { file = ../bin/restart-pipewire; })
    (mkScript "restart-waybar" { file = ../bin/restart-waybar; runtimeInputs = [ pkgs.waybar ]; })
    (mkScript "restart-wifi" { file = ../bin/restart-wifi; })
    (mkScript "screenshot-area" { file = ../bin/screenshot-area; runtimeInputs = [ pkgs.grim pkgs.slurp pkgs.wl-clipboard ]; })
    (mkScript "screenshot-save" { file = ../bin/screenshot-save; runtimeInputs = [ pkgs.grim pkgs.slurp ]; })
    (mkScript "screenshot-screen" { file = ../bin/screenshot-screen; runtimeInputs = [ pkgs.grim pkgs.wl-clipboard ]; })
    (mkScript "update" { file = ../bin/update; runtimeInputs = [ pkgs.alacritty pkgs.nix ]; })
    (mkScript "wallpaper" { file = ../bin/wallpaper; runtimeInputs = [ pkgs.fuzzel pkgs.sway pkgs.swaybg ]; })
  ];
}
