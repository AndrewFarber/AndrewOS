local diffview = require 'diffview'

diffview.setup {
  use_icons = true,
  view = {
    default = { layout = 'diff2_horizontal' },
    merge_tool = { layout = 'diff3_mixed' },
    file_history = { layout = 'diff2_horizontal' },
  },
}

local map = vim.keymap.set
map('n', '<leader>dv', '<cmd>DiffviewOpen<cr>', { desc = 'Diff view (uncommitted)' })
map('n', '<leader>df', '<cmd>DiffviewFileHistory %<cr>', { desc = 'Diff file history' })
map('n', '<leader>dh', '<cmd>DiffviewFileHistory<cr>', { desc = 'Diff repo history' })
map('n', '<leader>dc', '<cmd>DiffviewClose<cr>', { desc = 'Diff close' })
