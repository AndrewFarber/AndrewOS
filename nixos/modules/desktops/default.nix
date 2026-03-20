{ desktop, ... }:

let
  desktops = {
    sway = ./sway;
  };
in {
  imports = if desktops ? ${desktop} then [ desktops.${desktop} ] else [];
}
