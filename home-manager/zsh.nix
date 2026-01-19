{ userConfig, ... }:

{
  programs.zsh = {
    enable = true;
    shellAliases = {
      rebuild = "cd ~/AndrewOS && source .env && sudo -E nixos-rebuild switch --flake .#${userConfig.host} --impure";
      gc = "nix-collect-garbage -d";
      update = "cd ~/AndrewOS && nix flake update";
      ld = "lazydocker";
      lg = "lazygit";
      y = "yazi";
      ll = "eza --header --long --icons";
      lt = "eza --tree --icons";
      ta = "tmux attach-session";
      tk = "tmux kill-session";
      tl = "tmux list-sessions";
      tn = "tmux new-session";
      jupyter = "cd ~/AndrewOS && nix develop .#jupyter";
    };
    initContent = ''
      eval "$(direnv hook zsh)"
      eval "$(starship init zsh)"
    '';
  };
}
