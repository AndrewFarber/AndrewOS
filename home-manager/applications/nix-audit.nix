{ config, lib, pkgs, ... }:

let
  nix-audit = pkgs.python3Packages.buildPythonApplication {
    pname = "nix-audit";
    version = "0.1.0";
    pyproject = true;
    src = ../../tools/nix-audit;
    build-system = [ pkgs.python3Packages.setuptools ];
    dependencies = [ pkgs.python3Packages.textual ];
    nativeBuildInputs = [ pkgs.makeWrapper ];
    postFixup = ''
      wrapProgram $out/bin/nix-audit \
        --prefix PATH : ${lib.makeBinPath [ pkgs.home-manager pkgs.nix ]}
    '';
    doCheck = false; # tests need mocked nix/claude
  };
in
{
  options.andrewos.applications.nix-audit.enable =
    lib.mkEnableOption "Nix package security audit TUI";

  config = lib.mkIf config.andrewos.applications.nix-audit.enable {
    home.packages = [
      nix-audit
      pkgs.vulnix
    ];
  };
}
