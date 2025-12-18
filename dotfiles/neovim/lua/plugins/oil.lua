-- GitHub Repository: https://github.com/stevearc/oil.nvim
-- Description: A file explorer that lets you edit your filesystem like a buffer
require('oil').setup({
  default_file_explorer = true,
  columns = {
    'icon',
  },
  use_default_keymaps = true,
  view_options = {
    show_hidden = true,
  },
})

vim.keymap.set('n', '<leader>e', '<CMD>Oil<CR>', { desc = 'File Explorer' })
