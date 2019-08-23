-- use display-filter syntax here
local _filter = '(udp.port == 2000) && xml'

-- command to be executed for each packet
local _cmd = 'open /Applications/iTunes.app'
local _run = io.popen

local function make_tap(filter)
    local tap = Listener.new(nil, filter)

    function tap.packet()
        _run(_cmd)
    end

    return tap
end

-- If not running from Wireshark, enable the tap immediately, then
-- abort, or else we'll get an error below for trying to do GUI 
-- stuff from the command line.
if not gui_enabled() then
    make_tap(_filter)
    return
end

local function make_win()
    local tap = nil
    local win = TextWindow.new("Watcher")

    local function remove_tap()
    if tap then tap:remove() end
        tap = nil
    end

    win:set("Press Start to begin watching")
    win:set_atclose(remove_tap)

    win:add_button("Start", function()
        if tap then
            report_failure("Already started")
            return
        end

        win:set("Watching for:\\n" .. _filter)
        tap = make_tap(_filter)
    end)

    win:add_button("Stop", function()
        if not tap then
            report_failure("Not started")
            return
        end

        remove_tap()
        win:set("Press Start to begin watching")
    end)

    return win
end

register_menu("Lua/Test", make_win, MENU_TOOLS_UNSORTED or 8)