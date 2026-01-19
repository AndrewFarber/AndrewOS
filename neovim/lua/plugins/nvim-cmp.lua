-- GitHub Repository: https://github.com/hrsh7th/nvim-cmp
-- Description: Completion engine plugin for Neovim
local cmp = require('cmp')

cmp.setup({

  snippet = {
    expand = function(args)
      vim.fn['vsnip#anonymous'](args.body)
    end
  },

  mapping = cmp.mapping.preset.insert({
    ['<C-j>'] = cmp.mapping.select_next_item(),         -- go to next item
    ['<C-k>'] = cmp.mapping.select_prev_item(),         -- go to previous item
    ['<CR>'] = cmp.mapping.confirm { select = true },   -- complete selected item
  }),

  sources = cmp.config.sources(
    {
      { name = 'nvim_lsp' },
      { name = 'vsnip' },
    },
    {
      { name = 'buffers' },
    }
  ),

})

cmp.setup.cmdline({ '/', '?' }, {
  mapping = cmp.mapping.preset.cmdline({
    ['<C-j>'] = cmp.mapping(cmp.mapping.select_next_item(), { 'i', 'c' }),
    ['<C-k>'] = cmp.mapping(cmp.mapping.select_prev_item(), { 'i', 'c' }),
  }),
  sources = {
    { name = 'buffer' }
  }
})


cmp.setup.cmdline(':', {
  mapping = cmp.mapping.preset.cmdline({
    ['<C-j>'] = cmp.mapping(cmp.mapping.select_next_item(), { 'i', 'c' }),
    ['<C-k>'] = cmp.mapping(cmp.mapping.select_prev_item(), { 'i', 'c' }),
  }),
  sources = cmp.config.sources({
    { name = 'path' }
  }, {
    { name = 'cmdline' }
  }),
  matching = { disallow_symbol_nonprefix_matching = false }
})

