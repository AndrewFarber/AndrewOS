{ pkgs, ... }:

{
  fonts = {
    packages = with pkgs; [
      nerd-fonts.meslo-lg
      noto-fonts
      noto-fonts-cjk-sans
      noto-fonts-color-emoji
      font-awesome
    ];
  };
}
