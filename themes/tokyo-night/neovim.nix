{ pkgs, ... }:

{
  programs.neovim.plugins = with pkgs.vimPlugins; [
    tokyonight-nvim
  ];
}
