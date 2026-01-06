{ pkgs, ... }:

{
  virtualisation = {
    docker.enable = true;
    docker.extraPackages = [
      pkgs.docker-buildx
    ];
  };

  environment.systemPackages = with pkgs; [
    docker-compose
  ];
}
