-- Core settings
require 'core.options'  -- Load options
require 'core.keymaps'  -- Load keymaps

-- Plugins (downloaded using Nix Home-Manager)
require 'plugins.comment'
require 'plugins.dap'
require 'plugins.gitsigns'
require 'plugins.harpoon'
require 'plugins.lualine'
require 'plugins.noice'
require 'plugins.nvim-autopairs'
require 'plugins.nvim-cmp'
require 'plugins.nvim-lspconfig'
require 'plugins.nvim-treesitter'
require 'plugins.oil'
require 'plugins.telescope'
require 'plugins.which-key'

-- Theme (loaded from ~/.config/nvim/theme.lua, managed by NixOS)
dofile(vim.fn.stdpath('config') .. '/theme.lua')

