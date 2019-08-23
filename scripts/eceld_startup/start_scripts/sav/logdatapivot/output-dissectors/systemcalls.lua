-- systemcalls frame number-based postdissector
-- declare Fields to be read
-- declare our (pseudo) protocol
systemcalls_proto = Proto("systemcalls","systemcalls Log")
-- create the fields for our "protocol"
timestamp_F = ProtoField.string("systemcalls.timestamp","Original Event Timestamp")
eventdata_F = ProtoField.string("systemcalls.data","Data")

-- add the field to the protocol
systemcalls_proto.fields = {timestamp_F, eventdata_F}

-- create a function to "postdissect" each frame
function systemcalls_proto.dissector(buffer,pinfo,tree)
    -- add the data based on timestamps
    if pinfo.abs_ts >= 1508953280.0 and pinfo.abs_ts <= 1508953282.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("touch /tmp/snoopy.log ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:20"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953280.0 and pinfo.abs_ts <= 1508953282.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("tail -f /tmp/snoopy.log ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:20"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953281.0 and pinfo.abs_ts <= 1508953283.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("uname -p ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:21"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953282.0 and pinfo.abs_ts <= 1508953284.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("gnome-terminal ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953282.0 and pinfo.abs_ts <= 1508953284.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("gnome-terminal ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953282.0 and pinfo.abs_ts <= 1508953284.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("gnome-terminal ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953282.0 and pinfo.abs_ts <= 1508953284.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("gnome-terminal ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953282.0 and pinfo.abs_ts <= 1508953284.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("/usr/lib/gnome-terminal/gnome-terminal-server ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953283.0 and pinfo.abs_ts <= 1508953285.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("bash ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:23"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953283.0 and pinfo.abs_ts <= 1508953285.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("tput setaf 1 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:23"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953283.0 and pinfo.abs_ts <= 1508953285.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("dircolors -b ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:23"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953283.0 and pinfo.abs_ts <= 1508953285.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ls /etc/bash_completion.d ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:23"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953294.0 and pinfo.abs_ts <= 1508953296.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ifconfig eth0 10.0.0.2/24 up ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:34"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953302.0 and pinfo.abs_ts <= 1508953304.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("nmap 10.0.0.0-255 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:42"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953310.0 and pinfo.abs_ts <= 1508953312.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("dumpcap -i eth0 -w /root/ecel/plugins/collectors/tshark/raw/1508953280_eth0.pcap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:50"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953310.0 and pinfo.abs_ts <= 1508953312.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("dumpcap -i eth0 -w /root/ecel/plugins/collectors/tshark/raw/1508953280_eth0.pcap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:50"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953310.0 and pinfo.abs_ts <= 1508953312.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("dumpcap -i eth0 -w /root/ecel/plugins/collectors/tshark/raw/1508953280_eth0.pcap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:50"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953310.0 and pinfo.abs_ts <= 1508953312.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("dumpcap -i eth0 -w /root/ecel/plugins/collectors/tshark/raw/1508953280_eth0.pcap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:50"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953318.0 and pinfo.abs_ts <= 1508953320.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("route add default gw 10.0.0.1 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:41:58"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953322.0 and pinfo.abs_ts <= 1508953324.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("firefox-esr ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953322.0 and pinfo.abs_ts <= 1508953324.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("firefox-esr ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953322.0 and pinfo.abs_ts <= 1508953324.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("firefox-esr ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953322.0 and pinfo.abs_ts <= 1508953324.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("firefox-esr ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953349.0 and pinfo.abs_ts <= 1508953351.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("man nmap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953350.0 and pinfo.abs_ts <= 1508953352.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("locale charmap ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953350.0 and pinfo.abs_ts <= 1508953352.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("groff -mtty-char -Tutf8 -mandoc -rLL=205n -rLT=205n ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953367.0 and pinfo.abs_ts <= 1508953369.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("nmap 10.0.0-4.0-255 -p 80,80 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:42:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("msfconsole ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("egrep -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953409.0 and pinfo.abs_ts <= 1508953411.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("grep -E -q /usr/share/metasploit-framework/vendor/bundle ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:29"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953410.0 and pinfo.abs_ts <= 1508953412.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ruby /usr/bin/msfconsole ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953410.0 and pinfo.abs_ts <= 1508953412.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ruby /usr/bin/msfconsole ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953410.0 and pinfo.abs_ts <= 1508953412.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ruby /usr/bin/msfconsole ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953410.0 and pinfo.abs_ts <= 1508953412.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("ruby /usr/bin/msfconsole ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953410.0 and pinfo.abs_ts <= 1508953412.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("git --version ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:30"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("infocmp -C ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("infocmp -C -r ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("infocmp -C -r ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty size ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("infocmp -C -r ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953420.0 and pinfo.abs_ts <= 1508953422.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953437.0 and pinfo.abs_ts <= 1508953439.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:43:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953459.0 and pinfo.abs_ts <= 1508953461.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:19"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953459.0 and pinfo.abs_ts <= 1508953461.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:19"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953459.0 and pinfo.abs_ts <= 1508953461.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:19"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953459.0 and pinfo.abs_ts <= 1508953461.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:19"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953459.0 and pinfo.abs_ts <= 1508953461.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:19"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953480.0 and pinfo.abs_ts <= 1508953482.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:40"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953484.0 and pinfo.abs_ts <= 1508953486.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:44"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953494.0 and pinfo.abs_ts <= 1508953496.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:44:54"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953500.0 and pinfo.abs_ts <= 1508953502.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:00"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953501.0 and pinfo.abs_ts <= 1508953503.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("debian-sa1 1 1 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:01"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953502.0 and pinfo.abs_ts <= 1508953504.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953503.0 and pinfo.abs_ts <= 1508953505.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953503.0 and pinfo.abs_ts <= 1508953505.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953503.0 and pinfo.abs_ts <= 1508953505.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953503.0 and pinfo.abs_ts <= 1508953505.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953503.0 and pinfo.abs_ts <= 1508953505.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953510.0 and pinfo.abs_ts <= 1508953512.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:10"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953532.0 and pinfo.abs_ts <= 1508953534.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:32"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953532.0 and pinfo.abs_ts <= 1508953534.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:32"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953532.0 and pinfo.abs_ts <= 1508953534.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:32"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953532.0 and pinfo.abs_ts <= 1508953534.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:32"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953532.0 and pinfo.abs_ts <= 1508953534.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:45:32"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953562.0 and pinfo.abs_ts <= 1508953564.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:02"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953566.0 and pinfo.abs_ts <= 1508953568.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:06"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953576.0 and pinfo.abs_ts <= 1508953578.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:16"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953597.0 and pinfo.abs_ts <= 1508953599.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:37"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953599.0 and pinfo.abs_ts <= 1508953601.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953599.0 and pinfo.abs_ts <= 1508953601.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953599.0 and pinfo.abs_ts <= 1508953601.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953599.0 and pinfo.abs_ts <= 1508953601.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953599.0 and pinfo.abs_ts <= 1508953601.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:39"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953607.0 and pinfo.abs_ts <= 1508953609.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:47"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953617.0 and pinfo.abs_ts <= 1508953619.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:46:57"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953623.0 and pinfo.abs_ts <= 1508953625.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:03"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953634.0 and pinfo.abs_ts <= 1508953636.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:14"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953634.0 and pinfo.abs_ts <= 1508953636.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:14"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953634.0 and pinfo.abs_ts <= 1508953636.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:14"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953634.0 and pinfo.abs_ts <= 1508953636.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:14"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953634.0 and pinfo.abs_ts <= 1508953636.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:14"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953642.0 and pinfo.abs_ts <= 1508953644.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953646.0 and pinfo.abs_ts <= 1508953648.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:26"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953671.0 and pinfo.abs_ts <= 1508953673.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:47:51"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953690.0 and pinfo.abs_ts <= 1508953692.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:10"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953690.0 and pinfo.abs_ts <= 1508953692.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:10"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953691.0 and pinfo.abs_ts <= 1508953693.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:11"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953691.0 and pinfo.abs_ts <= 1508953693.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:11"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953691.0 and pinfo.abs_ts <= 1508953693.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:11"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953691.0 and pinfo.abs_ts <= 1508953693.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:11"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953698.0 and pinfo.abs_ts <= 1508953700.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:18"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty 4500:5:bf:8a3b:3:1c:7f:15:4:0:1:0:11:13:1a:0:12:f:17:16:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0 ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -g ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -a ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
    if pinfo.abs_ts >= 1508953702.0 and pinfo.abs_ts <= 1508953704.0 then
       local subtree = tree:add(systemcalls_proto,"systemcalls Log")
       local mycomplientstr = tostring("stty -echo -icrnl cbreak pass8 -ixoff ")

       subtree:add(tostring("Original Timestamp: "),tostring("2017-10-25T17:48:22"))
       subtree:add(tostring("Log Data: "), mycomplientstr)
    end
end
-- register our protocol as a postdissector
register_postdissector(systemcalls_proto)