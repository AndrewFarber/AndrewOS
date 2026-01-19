{ pkgs }:

let
  theme = "tokyo-night";  # Change this one line to switch themes
in
{
  name = theme;

  # Neovim module to import
  neovimModule = import ./${theme}/neovim.nix;

  # Lua config path for neovim theme
  neovimLua = ./${theme}/tokyonight.lua;

}
