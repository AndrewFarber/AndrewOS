-- GitHub Repository: https://github.com/nvim-treesitter/nvim-treesitter
-- Description: Syntax tree parser

-- Enable treesitter highlighting for all filetypes with available parsers
vim.api.nvim_create_autocmd('FileType', {
  callback = function()
    pcall(vim.treesitter.start)
  end,
})

-- Textobjects (https://github.com/nvim-treesitter/nvim-treesitter-textobjects)
require('nvim-treesitter-textobjects').setup({
  select = {
    lookahead = true,
    include_surrounding_whitespace = false,
  },
  move = {
    set_jumps = false,
  },
})

local select_ts = function(query)
  return function()
    require('nvim-treesitter-textobjects.select').select_textobject(query, 'textobjects')
  end
end

local move = require('nvim-treesitter-textobjects.move')

-- Select keymaps
local select_maps = {
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
}

for key, opts in pairs(select_maps) do
  vim.keymap.set({ 'x', 'o' }, key, select_ts(opts.query), { desc = opts.desc })
end

-- Move keymaps
local move_maps = {
  -- goto_next_start
  { "]f", "goto_next_start", "@function.outer", "Next function start" },
  { "]c", "goto_next_start", "@class.outer", "Next class start" },
  { "]p", "goto_next_start", "@parameter.inner", "Next parameter" },
  { "]s", "goto_next_start", "@local.scope", "Next scope" },
  -- goto_next_end
  { "]F", "goto_next_end", "@function.outer", "Next function end" },
  { "]C", "goto_next_end", "@class.outer", "Next class end" },
  -- goto_previous_start
  { "[f", "goto_previous_start", "@function.outer", "Previous function start" },
  { "[c", "goto_previous_start", "@class.outer", "Previous class start" },
  { "[p", "goto_previous_start", "@parameter.inner", "Previous parameter" },
  { "[s", "goto_previous_start", "@local.scope", "Previous scope" },
  -- goto_previous_end
  { "[F", "goto_previous_end", "@function.outer", "Previous function end" },
  { "[C", "goto_previous_end", "@class.outer", "Previous class end" },
  -- goto_next / goto_previous
  { "]i", "goto_next_start", "@conditional.outer", "Next conditional" },
  { "[i", "goto_previous_start", "@conditional.outer", "Previous conditional" },
}

for _, m in ipairs(move_maps) do
  vim.keymap.set({ 'n', 'x', 'o' }, m[1], function()
    move[m[2]](m[3], 'textobjects')
  end, { desc = m[4] })
end
