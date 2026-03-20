{ theme, ... }:

{
  programs.btop = {
    enable = true;
    settings = {
      color_theme = theme.btopTheme;
      theme_background = false;
    };
  };
}
