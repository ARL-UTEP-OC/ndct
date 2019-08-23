-- command to be executed for each packet
local _cmd = '/root/git/eceld-traffic-validator/scripts/validate.sh'
-- local _cmd = 'ls'

local function make_win()
    local win = TextWindow.new("Scoring")

    win:set("Check your score")
    local alllines = ''
    win:add_button("Score Me", function()
        win:set("Processing, please wait...")
        f = assert (io.popen (_cmd))
  
        for line in f:lines() do
            alllines = ( alllines .. line .. '\r\n')
        end -- for loop
        
        f:close()
        win:set(alllines)
    end)

    return win
end

register_menu("Lua/Score Comments", make_win, MENU_TOOLS_UNSORTED or 8)