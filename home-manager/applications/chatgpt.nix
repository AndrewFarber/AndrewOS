{ config, lib, pkgs, ... }:

{
  options.andrewos.applications.chatgpt.enable = lib.mkEnableOption "ChatGPT";

  config = lib.mkIf config.andrewos.applications.chatgpt.enable {
    xdg.desktopEntries.chatgpt = {
      name = "ChatGPT";
      comment = "ChatGPT by OpenAI";
      exec = "${pkgs.chromium}/bin/chromium --app=https://chatgpt.com";
      icon = "${../../assets/icons/chatgpt.png}";
      terminal = false;
      categories = [ "Network" ];
    };
  };
}
