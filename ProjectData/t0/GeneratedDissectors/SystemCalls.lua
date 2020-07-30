-- SystemCalls frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
SystemCalls_proto = Proto("SystemCalls","SystemCalls Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("SystemCalls.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("SystemCalls.data","Data")

-- add the field to the protocol
SystemCalls_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function SystemCalls_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1596128790.0 and pinfo.abs_ts <= 1596128792.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("sudo cat /etc/passwd")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128791.0 and pinfo.abs_ts <= 1596128793.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("cat /etc/passwd")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:31"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("service /usr/sbin/service auditd stop")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("basename /usr/sbin/service")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("basename /usr/sbin/service")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("systemctl --quiet is-active multi-user.target")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("systemctl list-unit-files --full multi-user.target")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("xhost -SI:localuser:root")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("sed -ne s/.sockets*[a-z]*s*$/.socket/p")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("auditd_parser.s bash /home/kali/eceld-netsys/eceld/plugins/parsers/auditd/auditd_parser.sh /home/kali/eceld-netsys/eceld/plugins/collectors/auditd/raw /home/kali/eceld-netsys/eceld/plugins/collectors/auditd/parsed")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("bash /home/kali/eceld-netsys/eceld/plugins/parsers/auditd/auditd_parser.sh /home/kali/eceld-netsys/eceld/plugins/collectors/auditd/raw /home/kali/eceld-netsys/eceld/plugins/collectors/auditd/parsed")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128807.0 and pinfo.abs_ts <= 1596128809.0 then
       local subtree = tree:add(SystemCalls_proto,"SystemCalls Log")
       local mycomplientstr = tostring("cat /home/kali/eceld-netsys/eceld/plugins/collectors/auditd/raw/1596128775_auditd.txt")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(SystemCalls_proto)