local km = vim.keymap
local dap = require("dap")
local dap_ui = require("dapui")
local dap_python = require("dap-python")

dap_ui.setup()

dap_python.setup("python")
dap_python.test_runner = "pytest"

dap.listeners.after.event_initialized["dapui_config"] = function()
  dap_ui.open()
end
dap.listeners.before.event_terminated["dapui_config"] = function()
  dap_ui.close()
end
dap.listeners.before.event_exited["dapui_config"] = function()
  dap_ui.close()
end

km.set("n", "<F5>", function() dap.continue() end)
km.set("n", "<F10>", function() dap.step_over() end)
km.set("n", "<F11>", function() dap.step_into() end)
km.set("n", "<F12>", function() dap.step_out() end)
km.set("n", "<Leader>b", function() dap.toggle_breakpoint() end)
km.set("n", "<Leader>B", function()
  dap.set_breakpoint(vim.fn.input("Breakpoint condition: "))
end)
