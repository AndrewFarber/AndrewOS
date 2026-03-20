{ desktop, ... }:

let
  desktops = {
    hyprland = ./hyprland;
    sway = ./sway;
  };
in {
  imports = if desktops ? ${desktop} then [ desktops.${desktop} ] else [];
}
