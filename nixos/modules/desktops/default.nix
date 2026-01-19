{ desktop, ... }:

let
  desktops = {
    gnome = ./gnome;
    hyprland = ./hyprland;
    plasma6 = ./plasma6;
    sway = ./sway;
  };
in {
  imports = if desktops ? ${desktop} then [ desktops.${desktop} ] else [];
}
