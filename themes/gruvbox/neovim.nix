{ pkgs, ... }:

{
  programs.neovim.plugins = with pkgs.vimPlugins; [
    gruvbox-nvim
  ];
}
