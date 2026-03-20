{ inputs, userConfig, desktop ? "", ... }:

let
  username = userConfig.username;
in

{
  imports = [ inputs.home-manager.nixosModules.home-manager ];

  home-manager = {
    useUserPackages = true;
    useGlobalPkgs = true;
    backupFileExtension = "backup";
    extraSpecialArgs = { inherit userConfig desktop; };
    users.${username} = {
      imports = [ ../../../home-manager/home.nix ];
    };
  };
}
