{ pkgs, ... }:

{
  nixpkgs.config.allowUnfree = true;
  programs = {
    chromium = {
      enable = true;
      extensions = [
        "dbepggeogbaibhgnhhndojpepiihcmeb"  # Vimium
        "ghmbeldphafepmbegfdlkpapadhbakde"  # Proton PW Manager
      ];
    };
    zsh.enable = true;
  };
  environment.systemPackages = with pkgs; [
    claude-code
    obsidian
  ];
}
