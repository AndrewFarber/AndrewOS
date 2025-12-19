{ pkgs, ... }:

{
  nixpkgs.config.allowUnfree = true;
  programs = {
    chromium = {
      enable = true;
      extensions = [
        "dbepggeogbaibhgnhhndojpepiihcmeb"
      ];
    };
    zsh.enable = true;
  };
  environment.systemPackages = with pkgs; [
    chromium
    claude-code
  ];
}
