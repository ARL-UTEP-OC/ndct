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
    if pinfo.abs_ts >= 1594056465.0 and pinfo.abs_ts <= 1594056467.0 then
       local subtree = tree:add(Keypresses_proto,"Keypresses Log")
       local mycomplientstr = tostring(" sd")

       subtree:add(tostring("Original Timestamp: "),tostring("2020-07-06T17:27:45"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(Keypresses_proto)