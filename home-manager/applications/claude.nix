{ config, lib, ... }:

{
  options.andrewos.applications.claude.enable = lib.mkEnableOption "Claude";

  config = lib.mkIf config.andrewos.applications.claude.enable {
    xdg.desktopEntries.claude = {
      name = "Claude";
      comment = "Claude by Anthropic";
      exec = "andrewos-launch-claude";
      icon = "${../../assets/icons/claude.png}";
      terminal = false;
      categories = [ "Network" ];
    };
  };
}
