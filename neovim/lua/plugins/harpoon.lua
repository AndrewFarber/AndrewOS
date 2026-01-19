-- GitHub Repository: https://github.com/ThePrimeagen/harpoon/tree/harpoon2
-- Description: Better marks
local harpoon = require('harpoon')

harpoon.setup({})

vim.keymap.set('n', '<leader>m', function() harpoon.ui:toggle_quick_menu(harpoon:list()) end, { desc = 'Harpoon Menu' })
vim.keymap.set('n', '<leader>a', function() harpoon:list():add() end, { desc = 'Harpoon Add' })

