{ pkgs, inputs, userConfig, ... }:

let
  username = userConfig.username;
in

{

  imports = [ inputs.home-manager.nixosModules.home-manager ];

  users.mutableUsers = true;
  users.users.${username} = {
    isNormalUser = true;
    extraGroups = [
      "docker"
      "networkmanager"
      "scanner"
      "wheel"
    ];
    shell = pkgs.zsh;
  };
  nix.settings.allowed-users = [ username ];

  home-manager = {
    useUserPackages = true;
    useGlobalPkgs = false;
    backupFileExtension = "backup";
    extraSpecialArgs = { inherit userConfig; };
    users.${username} = {
      imports = [ ./../home-manager/home.nix ];
    };
  };
}
