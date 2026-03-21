{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.claude-code.enable = lib.mkEnableOption "Claude Code AI assistant";

  config = lib.mkIf config.andrewos.applications.claude-code.enable {
    home.packages = with pkgs; [
      claude-code
    ];
  };
}
