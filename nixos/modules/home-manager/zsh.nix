{ ... }:

{
  programs.zsh = {
    enable = true;
    shellAliases = {
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
