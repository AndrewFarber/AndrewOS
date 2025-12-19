{ pkgs, ... }:

{
  nixpkgs.config.allowUnfree = true;
  programs = {
    firefox.enable = true;
    zsh.enable = true;
  };
  environment.systemPackages = with pkgs; [ 
    claude-code
  ];
}
