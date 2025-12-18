-- [[ Options ]]

-- Nerd font
vim.g.have_nerd_font = true

local opt = vim.opt

-- Line numbers
opt.number = true           -- add line numbers
opt.relativenumber = true   -- relative line numbers

-- Tabs and indentation
opt.tabstop = 2             -- 4 spaces for tabs
opt.shiftwidth = 2          -- 4 spaces for indent width
opt.expandtab = true        -- expand tabs to spaces
opt.autoindent = true       -- copy indent from current line when starting new line

-- Appearance
opt.showmode = false        -- show mode below status bar
opt.signcolumn = 'yes'      -- always include column left of line numbers
opt.cursorline = true       -- highlight the text line of the cursor
opt.scrolloff = 10          -- min number of screen lines to keep above and below the cursor
opt.background = "dark"     -- color schemes setting

-- Line wrap
opt.wrap = true             -- wrap text to next line
opt.breakindent = true      -- if text wraps, visually indent

-- Searching
opt.ignorecase = true       -- ignore case when searching
opt.smartcase = true        -- if you include mix case in search, assume you want case-sensitive

-- Key press timing
opt.timeoutlen = 400        -- mapped sequence time out (milliseconds)

-- Splits
opt.splitright = true       -- split vertical window to the right
opt.splitbelow = true       -- split horizontal window to the bottom

-- White space characters
opt.list = true             -- update how white space characters are rendered
opt.listchars = {           -- white space overrides
    tab = '» ',
    trail = '·',
    nbsp = '␣',
    space = '·'
}

-- Spelling
opt.spell = true            -- turn on spelling help
opt.spelllang = 'en_us'     -- set spelling dictionary to US English

