-- GitHub Repository: https://github.com/nvim-lualine/lualine.nvim
-- Description: Configurable Neovim statusline
require('lualine').setup({
  sections = {
    lualine_a = {'mode'},
    lualine_b = {'branch', 'diff', 'diagnostics'},
    lualine_c = {},
    lualine_x = {'encoding', 'fileformat', 'filetype'},
    lualine_y = {'progress'},
    lualine_z = {'location'}
  },
  winbar = {
    lualine_a = { {"filename", path = 3} },
    lualine_c = { { "navic", color_correction = nil, navic_opts = nil } }
  }
})

