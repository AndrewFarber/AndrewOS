{ config, lib, ... }:

{
  options.andrewos.applications.chatgpt.enable = lib.mkEnableOption "ChatGPT";

  config = lib.mkIf config.andrewos.applications.chatgpt.enable {
    xdg.desktopEntries.chatgpt = {
      name = "ChatGPT";
      comment = "ChatGPT by OpenAI";
      exec = "andrewos-launch-chatgpt";
      icon = "${../../assets/icons/chatgpt.png}";
      terminal = false;
      categories = [ "Network" ];
    };
  };
}
