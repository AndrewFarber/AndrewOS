{
  description = "AndrewOS";

  inputs = {
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... } @ inputs:
    let
      system = "x86_64-linux";
      userConfig = {
        username = builtins.getEnv "USERNAME";
        fullName = builtins.getEnv "GIT_FULL_NAME";
        email = builtins.getEnv "GIT_EMAIL";
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

      # Nix Shells
      # nix develop .#python
      devShells.${system} = {
        python = import ./shells/python.nix { inherit pkgs; };
      };

    };
}
