-- GitHub Repository: https://github.com/nvim-telescope/telescope.nvim
-- Description: Fuzzy finder
require('telescope').setup({
  extensions = {
    ['ui-select'] = {
      require('telescope.themes').get_dropdown(),
    },
  },
  defaults = {
    mappings = {
      i = {
        ['<C-k>'] = {
          require('telescope.actions').move_selection_previous,
          type = 'action',
          opts = { silent = true, nowait = true },
        },
        ['<C-j>'] = {
          require('telescope.actions').move_selection_next,
          type = 'action',
          opts = { silent = true, nowait = true },
        },
      },
    }
  },
})

pcall(require('telescope').load_extension, 'fzf')
pcall(require('telescope').load_extension, 'ui-select')
local builtin = require('telescope.builtin')
local km = vim.keymap

km.set('n', '<leader>ff', builtin.find_files, { desc = 'Find Files' })
km.set('n', '<leader>fs', builtin.live_grep, { desc = 'Find String' })
km.set('n', '<leader>fb', builtin.buffers, { desc = 'Find Buffers' })
km.set('n', '<leader>fr', builtin.registers, { desc = 'Find Registers' })
km.set('n', '<leader>fm', builtin.marks, { desc = 'Find Marks' })
km.set('n', '<leader>fq', builtin.quickfix, { desc = 'Find Quickfix' })
km.set('n', '<leader>fk', builtin.keymaps, { desc = 'Find Keymaps' })
km.set('n', '<leader>fz', builtin.spell_suggest, { desc = 'Find Spelling Suggestions' })

km.set('n', '<leader>/', function()
  builtin.current_buffer_fuzzy_find(require('telescope.themes').get_dropdown {
    winblend = 10,
    previewer = false,
  })
end, { desc = 'Fuzzily Search' })
