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
      extraOpts = {
        # Privacy
        BrowserSignin = 0;
        SyncDisabled = true;
        MetricsReportingEnabled = false;
        SpellCheckServiceEnabled = false;
        PasswordManagerEnabled = false;
        AutofillAddressEnabled = false;
        AutofillCreditCardEnabled = false;

        # Security
        HttpsOnlyMode = "force_enabled";

        # Startup
        # RestoreOnStartup = 1;
      };
    };
    zsh.enable = true;
  };
  environment.systemPackages = with pkgs; [
    chromium
    claude-code
    obsidian
  ];
}
