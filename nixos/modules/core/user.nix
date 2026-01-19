{ pkgs, userConfig, ... }:

let
  username = userConfig.username;
in

{
  users.mutableUsers = true;
  users.users.${username} = {
    isNormalUser = true;
    extraGroups = [
      "docker"
      "scanner"
      "wheel"
    ];
    shell = pkgs.zsh;
  };
  nix.settings.allowed-users = [ username ];
}
