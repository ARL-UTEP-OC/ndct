-- Keypresses frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
Keypresses_proto = Proto("Keypresses","Keypresses Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("Keypresses.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("Keypresses.data","Data")

-- add the field to the protocol
Keypresses_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function Keypresses_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1596128791.0 and pinfo.abs_ts <= 1596128793.0 then
       local subtree = tree:add(Keypresses_proto,"Keypresses Log")
       local mycomplientstr = tostring("[Up][Up][Up][Up][Down][Down][Down][Down][Down]sudo cat /etc/passwd[Return]kali[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:31"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128799.0 and pinfo.abs_ts <= 1596128801.0 then
       local subtree = tree:add(Keypresses_proto,"Keypresses Log")
       local mycomplientstr = tostring("ping google.com[Return]")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1596128804.0 and pinfo.abs_ts <= 1596128806.0 then
       local subtree = tree:add(Keypresses_proto,"Keypresses Log")
       local mycomplientstr = tostring("[Control_L]")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-30T17:06:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(Keypresses_proto)