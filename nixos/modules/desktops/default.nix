{ desktop, ... }:

let
  desktops = {
    gnome = ./gnome;
    plasma6 = ./plasma6;
  };
in {
  imports = if desktops ? ${desktop} then [ desktops.${desktop} ] else [];
}
