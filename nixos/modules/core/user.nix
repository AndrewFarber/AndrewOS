{ pkgs, inputs, userConfig, desktop ? "", ... }:

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
    extraSpecialArgs = { inherit userConfig desktop; };
    users.${username} = {
      imports = [ ./../home-manager/home.nix ];
    };
  };
}
