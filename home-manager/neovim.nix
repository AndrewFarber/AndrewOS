{ pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;
    extraPackages = [ pkgs.gcc pkgs.nodejs ];
    plugins = with pkgs.vimPlugins; [

      # Dependencies
      cmp-buffer
      cmp-cmdline
      cmp-nvim-lsp
      cmp-path
      cmp-vsnip
      nui-nvim
      nvim-dap-python
      nvim-dap-ui
      nvim-notify
      nvim-web-devicons
      plenary-nvim
      telescope-fzf-native-nvim
      telescope-ui-select-nvim
      vim-vsnip

      # Core
      comment-nvim
      gitsigns-nvim
      harpoon2
      lualine-nvim
      noice-nvim
      nvim-autopairs
      nvim-cmp
      nvim-dap
      nvim-lspconfig
      nvim-navbuddy
      nvim-navic
      nvim-treesitter
      nvim-treesitter-textobjects
      (nvim-treesitter.withPlugins (p: [
        p.python
        p.nix
        p.lua
        p.markdown
        p.json
        p.regex
        p.bash
      ]))
      oil-nvim
      telescope-nvim
      vim-fugitive
      vim-sleuth
      vim-surround
      which-key-nvim

    ];
  };
}
