{
  description = "HydraOS";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, ... } @ inputs:
    let
      system = "x86_64-linux";
      userConfig = {
        username = builtins.getEnv "USERNAME";
        fullName = builtins.getEnv "NAME";
        email = builtins.getEnv "EMAIL";
        host = builtins.getEnv "HOST";
        desktop = builtins.getEnv "DESKTOP";
      };
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in {
      nixosConfigurations = {

        vbox-laptop = nixpkgs.lib.nixosSystem {
          inherit system;
          specialArgs = {
            host = userConfig.host;
            desktop = userConfig.desktop;
            inherit inputs userConfig;
          };
          modules = [ ./nixos/hosts/vbox-laptop ];
        };

        vbox-desktop = nixpkgs.lib.nixosSystem {
          inherit system;
          specialArgs = {
            host = userConfig.host;
            desktop = userConfig.desktop;
            inherit inputs userConfig;
          };
          modules = [ ./nixos/hosts/vbox-desktop ];
        };

      };

      devShells.${system} = {
        jupyter = import ./shells/jupyter.nix { inherit pkgs; };
      };

    };
}
