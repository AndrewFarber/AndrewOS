{ ... }:

let
  theme = import ./../../../themes/default.nix;
in
{
  imports = [
    ./fonts.nix
    ./home-manager.nix
    ./network.nix
    ./packages.nix
    ./system.nix
    ./user.nix
    ./virtualization.nix
    theme.stylixModule
  ];
}
