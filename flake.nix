{
  description = "AndrewOS";

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
      };
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in {
      nixosConfigurations = {
        vbox = nixpkgs.lib.nixosSystem {
          inherit system;
          specialArgs = {
            host = "vbox";
            desktop = "sway";
            inherit inputs userConfig;
          };
          modules = [ ./nixos/hosts/vbox ];
        };
      };

      devShells.${system} = {
        jupyter = import ./shells/jupyter.nix { inherit pkgs; };
      };

    };
}
