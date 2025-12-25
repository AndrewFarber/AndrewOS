{ ... }:

{
  programs.zsh = {
    enable = true;
    shellAliases = {
      rebuild = "cd ~/AndrewOS && source .env && sudo -E nixos-rebuild switch --flake .#vbox --impure";
      ld = "lazydocker";
      lg = "lazygit";
      ll = "eza --header --long --icons";
      lt = "eza --tree --icons";
      ta = "tmux attach-session";
      tk = "tmux kill-session";
      tl = "tmux list-sessions";
      tn = "tmux new-session";
    };
    initContent = ''
      eval "$(starship init zsh)"
    '';
  };
}
