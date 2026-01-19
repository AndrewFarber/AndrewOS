{ pkgs, ... }:

{
  programs.fuzzel = {
    enable = true;
    settings = {
      main = {
        font = "MesloLGS Nerd Font:size=12";
        width = 50;
        lines = 12;
        horizontal-pad = 20;
        vertical-pad = 15;
        icons-enabled = "yes";
        icon-theme = "hicolor";
        match-mode = "fzf";
        include = "~/.config/fuzzel/theme.ini";
      };
      border = {
        width = 2;
        radius = 8;
      };
      key-bindings = {
        prev = "Up Control+k";
        next = "Down Control+j";
      };
    };
  };

  # Hide apps from Fuzzel launcher
  xdg.desktopEntries = {
    nvim = {
      name = "Neovim wrapper";
      noDisplay = true;
    };
    yazi = {
      name = "Yazi";
      noDisplay = true;
    };
  };

}
