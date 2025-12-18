{ desktop, ... }:

let
  desktop_configuration = if desktop == "gnome" then ./gnome
                          else if desktop == "plasma6" then ./plasma6
                          else if desktop == "disabled" then ./disabled
                          else ./gnome;
in {
  imports = [ desktop_configuration ];
}
