-- GitHub Repository: https://github.com/nvim-treesitter/nvim-treesitter
-- Description: Syntax tree parser
require('nvim-treesitter.configs').setup({
  auto_install = false,
  highlight = {
    enable = true,
    additional_vim_regex_highlighting = false,
  },
  textobjects = {
    select = {
      enable = true,
      lookahead = true,
      keymaps = {
        ["if"] = { query = "@function.inner", desc = "Select inner function" },
        ["af"] = { query = "@function.outer", desc = "Select outer function" },
        ["ac"] = { query = "@class.outer", desc = "Select outer class" },
        ["ic"] = { query = "@class.inner", desc = "Select inner class" },
        ["ap"] = { query = "@parameter.outer", desc = "Select outer parameter" },
        ["ip"] = { query = "@parameter.inner", desc = "Select inner parameter" },
        ["ai"] = { query = "@conditional.outer", desc = "Select outer conditional" },
        ["ii"] = { query = "@conditional.inner", desc = "Select inner conditional" },
        ["al"] = { query = "@loop.outer", desc = "Select outer loop" },
        ["il"] = { query = "@loop.inner", desc = "Select inner loop" },
      },
      include_surrounding_whitespace = false,
    },
    move = {
      enable = true,
      set_jumps = false,
      goto_next_start = {
        ["]f"] = { query = "@function.outer", desc = "Next function start" },
        ["]c"] = { query = "@class.outer", desc = "Next class start" },
        ["]p"] = { query = "@parameter.inner", desc = "Next parameter" },
        ["]s"] = { query = "@local.scope", query_group = "locals", desc = "Next scope" },
      },
      goto_next_end = {
        ["]F"] = { query = "@function.outer", desc = "Next function end" },
        ["]C"] = { query = "@class.outer", desc = "Next class end" },
      },
      goto_previous_start = {
        ["[f"] = { query = "@function.outer", desc = "Previous function start" },
        ["[c"] = { query = "@class.outer", desc = "Previous class start" },
        ["[p"] = { query = "@parameter.inner", desc = "Previous parameter" },
        ["[s"] = { query = "@local.scope", query_group = "locals", desc = "Previous scope" },
      },
      goto_previous_end = {
        ["[F"] = { query = "@function.outer", desc = "Previous function end" },
        ["[C"] = { query = "@class.outer", desc = "Previous class end" },
      },
      goto_next = {
        ["]i"] = { query = "@conditional.outer", desc = "Next conditional" },
      },
      goto_previous = {
        ["[i"] = { query = "@conditional.outer", desc = "Previous conditional" },
      }
    },
    lsp_interop = {
      enable = true,
      border = 'none',
      floating_preview_opts = {},
      peek_definition_code = {
        ["<leader>df"] = { query = "@function.outer", desc = "Peek function" },
        ["<leader>dc"] = { query = "@class.outer", desc = "Peek class"},
      },
    },
  },
})
