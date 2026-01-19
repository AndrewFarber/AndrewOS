{ pkgs, ... }:

{
  home.packages = with pkgs; [
    lua-language-server       # Lua
    nil                       # Nix
    pyright                   # Python
  ];
}
