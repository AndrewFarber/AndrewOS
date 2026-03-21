{ config, lib, ... }:

{
  options.andrewos.applications.chromium.enable = lib.mkEnableOption "Chromium";

  config = lib.mkIf config.andrewos.applications.chromium.enable {
    programs.chromium = {
      enable = true;
      extensions = [
        { id = "dbepggeogbaibhgnhhndojpepiihcmeb"; }  # Vimium
        { id = "ghmbeldphafepmbegfdlkpapadhbakde"; }  # Proton PW Manager
      ];
    };
  };
}
