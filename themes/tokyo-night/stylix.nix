{ pkgs, inputs, ... }:

{
  imports = [ inputs.stylix.nixosModules.stylix ];

  stylix = {
    enable = true;

    # Tokyo Night color scheme
    base16Scheme = "${pkgs.base16-schemes}/share/themes/tokyo-night-storm.yaml";

    # Wallpaper (required by stylix, can use a solid color image)
    image = pkgs.runCommand "wallpaper" {} ''
      ${pkgs.imagemagick}/bin/magick -size 1920x1080 xc:#222436 $out
    '';

    # Fonts
    fonts = {
      monospace = {
        package = pkgs.nerd-fonts.meslo-lg;
        name = "MesloLGS Nerd Font";
      };
      sansSerif = {
        package = pkgs.inter;
        name = "Inter";
      };
      serif = {
        package = pkgs.dejavu_fonts;
        name = "DejaVu Serif";
      };
      sizes = {
        terminal = 12;
        applications = 11;
      };
    };

    # Opacity settings
    opacity = {
      terminal = 0.9;
    };

    # Cursor theme
    cursor = {
      package = pkgs.adwaita-icon-theme;
      name = "Adwaita";
      size = 24;
    };
  };

  # Disable neovim theming in home-manager (we manage init.lua ourselves)
  home-manager.sharedModules = [{
    stylix.targets.neovim.enable = false;
  }];
}
