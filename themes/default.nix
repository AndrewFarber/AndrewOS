let
  theme = "tokyo-night";  # Change this one line to switch themes
in
{
  name = theme;

  # Stylix module for NixOS
  stylixModule = ./${theme}/stylix.nix;
}
