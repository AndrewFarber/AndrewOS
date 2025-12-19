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
        # NixOS on Oracle VirtualBox
        # sudo nixos-rebuild switch --flake .#vbox
        vbox = nixpkgs.lib.nixosSystem {
          inherit system;
          specialArgs = {
            host = "vbox";
            desktop = "plasma6";
            inherit inputs userConfig;
          };
          modules = [ ./nixos/hosts/vbox ];
        };
      };

      # Home-Manager Stand Alone
      # home-manager switch --flake .
      homeConfigurations.${userConfig.username} = inputs.home-manager.lib.homeManagerConfiguration {
        inherit pkgs;
        extraSpecialArgs = { inherit userConfig; };
        modules = [ ./nixos/modules/home-manager/home.nix ];
      };

      # Nix Shells
      # nix develop .#python
      devShells.${system} = {
        python = import ./shells/python.nix { inherit pkgs; };
      };

    };
}
