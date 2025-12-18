{ userConfig, ... }:

{
  programs.git = {
    enable = true;
    settings.user.name = userConfig.fullName;
    settings.user.email = userConfig.email;
  };
  programs.gh = {
    enable = true;
    gitCredentialHelper = {
      enable = true;
    };
  };
}
