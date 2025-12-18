-- GitHub Repository: https://github.com/neovim/nvim-lspconfig
-- Description: "Data only" repository providing basic Neovim LSP defaults
local lspconfig = require('lspconfig')
local navic = require('nvim-navic')
local navbuddy = require('nvim-navbuddy')
local capabilities = require('cmp_nvim_lsp').default_capabilities()

local on_attach = function(client, bufnr)
  navic.attach(client, bufnr)
  navbuddy.attach(client, bufnr)
end

-- LSP configurations
lspconfig.pyright.setup({
  capabilities = capabilities,
  on_attach = on_attach,
})

lspconfig.nil_ls.setup({
  capabilities = capabilities,
  on_attach = on_attach,
})

lspconfig.lua_ls.setup({
  capabilities = capabilities,
  on_attach = on_attach,
  settings = {
    Lua = {
      diagnostics = {
        globals = { 'vim' }
      }
    }
  }
})

vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('lsp-attach', { clear = true }),

  callback = function(event)

    local telescope = require('telescope.builtin')

    local map = function(keys, func, desc, mode)
      mode = mode or 'n'
      vim.keymap.set(mode, keys, func, { buffer = event.buf, desc = desc })
    end

    -- Jump to the definition of the word under your cursor
    -- This is where a variable was first declared/defined/etc
    map('<leader>gd', telescope.lsp_definitions, 'Goto Definition')

    -- Find references for the word under your cursor
    map('<leader>gr', telescope.lsp_references, 'Goto References')

    -- Jump to the implementation of the word under your cursor
    -- Useful when your language has ways of declaring types without an actual implementation
    map('<leader>gi', telescope.lsp_implementations, 'Goto Implementation')

    -- Jump to the type of the word under your cursor
    -- Useful when your're not sure what type of variable is and you want to see
    -- the definition of its *type*, not where it was *defined*
    map('<leader>gt', telescope.lsp_type_definitions, 'Goto Type Definition')

    -- Fuzzy find all the symbols in your current document
    -- Symbols are things like variables, functions, types, etc.
    map('<leader>gs', telescope.lsp_document_symbols, 'Document Symbols')

    -- Fuzzy find all the symbols in your current workspace
    -- Similar to document symbols, except searches over your entire project
    map('<leader>gS', telescope.lsp_dynamic_workspace_symbols, 'Workspace Symbols')

    -- Rename word under cursor
    map('<leader>r', vim.lsp.buf.rename, 'Rename')

    -- Code actions
    map('<leader>c', vim.lsp.buf.code_action, 'Code Action', { 'n', 'x' })

    map('<leader>o', "<CMD>Navbuddy<CR>", "Outline")

    local client = vim.lsp.get_client_by_id(event.data.client_id)
    if client and client.supports_method(vim.lsp.protocol.Methods.textDocument_documentHighlight) then

      local highlight_augroup = vim.api.nvim_create_augroup('lsp-highlight', { clear = false })

      vim.api.nvim_create_autocmd({ 'CursorHold', 'CursorHoldI' }, {
        buffer = event.buf,
        group = highlight_augroup,
        callback = vim.lsp.buf.document_highlight,
      })

      vim.api.nvim_create_autocmd({ 'CursorMoved', 'CursorMovedI' }, {
        buffer = event.buf,
        group = highlight_augroup,
        callback = vim.lsp.buf.clear_references,
      })

      vim.api.nvim_create_autocmd('LspDetach', {
        group = vim.api.nvim_create_augroup('lsp-detach', { clear = true }),
        callback = function(event2)
        vim.lsp.buf.clear_references()
        vim.api.nvim_clear_autocmds { group = 'lsp-highlight', buffer = event2.buf }
      end })

    end

  end,
})
