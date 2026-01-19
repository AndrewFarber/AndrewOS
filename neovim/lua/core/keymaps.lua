-- [[ Keymaps ]]

local km = vim.keymap

-- Set leader key
vim.g.mapleader = ' '
vim.g.maplocalleader = ' '
km.set({'n', 'v'}, '<Space>', '<Nop>', { silent = true })

-- Clear highlights on search when pressing <Esc> in normal mode
km.set('n', '<Esc>', '<cmd>nohlsearch<CR>')

-- Delete single character without copying into register
km.set('n', 'x', '"_x', { desc = 'Delete character to right' })
km.set('n', 'X', '"_X', { desc = 'Delete character to left' })

-- Vertical scroll then center
km.set('n', '<C-d>', '<C-d>zz', { desc = 'Page down' })
km.set('n', '<C-u>', '<C-u>zz', { desc = 'Page up' })

-- Stay in indent mode
km.set('v', '<', '<gv', { desc = 'Indent' })
km.set('v', '>', '>gv', { desc = 'Outdent' })

-- Keep last yanked when pasting
km.set('v', 'p', '"_dP', { desc = 'Paste' })

-- Move lines up/down
km.set("n", "<A-j>", ":m .+1<CR>==")
km.set("n", "<A-k>", ":m .-2<CR>==")
km.set("v", "<A-j>", ":m '>+1<CR>gv=gv")
km.set("v", "<A-k>", ":m '<-2<CR>gv=gv")

