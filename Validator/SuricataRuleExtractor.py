#!/usr/bin/python2
import json
import logging
import os
import shutil
import shlex
import sys, traceback
import time
from jinja2 import Environment, FileSystemLoader
from subprocess import Popen
import subprocess

class SuricataRuleExtractor():
    
    def __init__(self):
        self.tcp_convo_counter = 0

    def json_to_rules(self, json_rules_filename):
        try:
            logging.debug("json_to_rules() instantiated")
            with open(json_rules_filename) as json_input:
                logging.debug("json_to_rules(): Reading comments")
                comments_json = json.load(json_input)
            #sample: alert tcp 10.0.2.2 8080 -> any any (msg: "Found"; content: "Module"; flags: PA; sid: 3; )
            suricata_rules = []
            suri_sid = 0
            for comment in comments_json:
                logging.debug("Comment: " + str(comment))
                suri_sid += 1
                protocol_dict = comment["id"]
                suri_proto = ""

                suri_msg = comment["description"] + " CMD-" + self.comply_string(comment["run-descriptor"])
                protocol_dict = comment["protocol"]

                if "eth:ethertype:ip" in protocol_dict:
                    suri_proto = "ip"
                    suri_ip_src = "any"
                    suri_sport = "any"
                    suri_direction = "->"
                    suri_ip_dest = "any"
                    suri_dport = "any"
                    suri_custom_attr = ""
                    
                    ip_dict = protocol_dict["eth:ethertype:ip"]
                    logging.debug("ip_dict:" + str(ip_dict))
                    if ip_dict["ip_src"]["keep"] == "true":
                        suri_ip_src = ip_dict["ip_src"]["val"]

                    if ip_dict["ip_dest"]["keep"] == "true":
                        suri_ip_dest = ip_dict["ip_dest"]["val"]
                    print("READ DIRECTION1: " + str(ip_dict["comm_mode"]))
                    if "single" in ip_dict["comm_mode"]:
                        print("READ DIRECTION2: " + str(ip_dict["comm_mode"]))
                        comm_mode_single_dict = ip_dict["comm_mode"]["single"]
                        print("READ DIRECTION3: " + str(comm_mode_single_dict))
                        if comm_mode_single_dict["direction"] == ">":
                            suri_direction = "->"
                        elif comm_mode_single_dict["direction"] == "<":
                            suri_direction = "<-"
                        elif comm_mode_single_dict["direction"] == "<>":
                            suri_direction = "<>"

                    elif "suricata-rule-attr" in ip_dict["comm_mode"]:
                        comm_mode_attr_dict = ip_dict["comm_mode"]["suricata-rule-attr"]
                        for attr in comm_mode_attr_dict:
                            suri_custom_attr += str(attr) + "; "

                    ##Write the rule as an IP rule
                    suricata_rule = "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                        + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                        + " (msg: \"" + suri_msg + "\"; " + suri_custom_attr + " sid:" + str(suri_sid) + ";)"

                    if "eth:ethertype:ip:icmp" in protocol_dict:
                        suri_proto = "icmp"
                        ##Write the rule as an ICMP rule
                        suricata_rule = "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                        + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                        + " (msg: \"" + suri_msg + "\"; " + suri_custom_attr + " sid:" + str(suri_sid) + ";)"

                    if "eth:ethertype:ip:tcp" in protocol_dict:
                        suri_proto = "tcp"
                        #Additional TCP-specific items
                        suri_flags = ""
                        suri_content = ""
                        
                        #Extract attributes for TCP
                        tcp_dict = protocol_dict["eth:ethertype:ip:tcp"]
                        
                        if tcp_dict["sport"]["keep"] == "true":
                            suri_sport = tcp_dict["sport"]["val"]

                        if tcp_dict["dport"]["keep"] == "true":
                            suri_dport = tcp_dict["dport"]["val"]
                    
                        #get specific flags and remove any non-printable characters
                        flags = tcp_dict["flags"]
                        flags = "".join([c if 0x21<=ord(c) and ord(c)<=0x7e else "" for c in flags])
                        if len(flags) != 0:
                            suri_flags = flags

                        #get content or leave blank if none
                        if "payload-identifier" in tcp_dict:
                            payload_identifier_dict = tcp_dict["payload-identifier"]
                            
                            suri_case = ""
                            if "casematters" in payload_identifier_dict:
                                casematters = payload_identifier_dict["casematters"]
                                if casematters == "false":
                                    suri_case = "nocase; "
                            
                            mypayload = str(payload_identifier_dict["payload"])
                            #Set content and make sure the strings are complient for suricata accordin to
                            #https://suricata.readthedocs.io/en/suricata-4.1.3/rules/payload-keywords.html
                            if payload_identifier_dict["type"] == "all" and len(mypayload) > 0:
                                #get the contents and format into suricata-required
                                suri_content = "\"|" + mypayload.replace(":"," ") + "|\""
                            elif payload_identifier_dict["type"] == "match":
                                #just paste user provided match string if not empty
                                if len(mypayload) == 0:
                                    suri_content = ""
                                else:
                                    suri_content = "\"" + self.comply_string(mypayload) + "\""
                            #either all or match selected, but no data provided; so default to "ignore"
                            else: 
                                suri_content = ""
                            if suri_content != "":
                                suri_content = suri_case + suri_content


                        #case when user wants a conversation, we need to construct a set of rules, not just one; 
                        #TODO: don't assume we have the first PA packet
                        #alert tcp 10.0.2.2 any -> any any (msg: "Illegitimate Connection Start 3-way Handshake"; flow: to_server; flowint:count2, notset; flowint:count2,=,1; flags: S; sid: 5; )
                        #alert tcp 10.0.2.2 any -> any any (msg: "Illegitimate Connection Start Conn Established"; flow: to_server; flowint:count2, isset; flowint: count2,==,1; flowint: count2, +, 1; flags: PA; content: "GET "; sid: 7; )
                        #alert tcp any any -> 10.0.2.2 any (msg: "Illegitimate Connection Stopped Abruptly by Server"; flags: R; flowint:count2, isset; sid: 9; )
                        #alert tcp 10.0.2.2 any -> any any (msg: "Illegitimate Connection Stopped Abruptly by Client"; flags: R; flowint:count2, isset; sid: 10; )
                        #alert tcp 10.0.2.2 any -> any any (msg: "Illegitimate Connection Conn Closed"; flags: FA; flowint:count2, isset; sid: 11; )
                        if ip_dict["comm_mode"] == "conversation":
                            self.tcp_convo_counter += 1
                            tcpConvoCounterVarName = "tcp_convo_counter"+ str(self.tcp_convo_counter)
                            ####SYN####
                            suricata_rule = "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                            + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                            + " (msg: \"Start 3-way TCP-" + suri_msg + "\"; " \
                            + "flow: to_server; flowint:  "+ tcpConvoCounterVarName+", notset; flowint: " +tcpConvoCounterVarName+",=,1; flags: S; " \
                            " sid: " + str(suri_sid) + ";)"
                            suri_sid += 1
                            suricata_rule += "\r\n"
                            ####First Data Packet (PSH+ACK)
                            suricata_rule += "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                            + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                            + " (msg: \"Conn Established-" + suri_msg + "\"; " \
                            + "flow: to_server; flowint:  "+ tcpConvoCounterVarName+", isset; flowint: " +tcpConvoCounterVarName+",==,1; flowint: " + tcpConvoCounterVarName + ", +, 1; flags: PA; "
                            if suri_content != "":    
                                suricata_rule += "content:" + suri_content + ";" 
                            suricata_rule += " flags: " + suri_flags + "; " + suri_custom_attr + " sid: " + str(suri_sid) + ";)"
                            suri_sid += 1
                            suricata_rule += "\r\n"
                            ####Reset Packet from Server
                            suricata_rule += "alert " + suri_proto + " " + suri_ip_dest + " " + suri_dport + " " \
                            + suri_direction + " " + suri_ip_src + " " + suri_sport \
                            + " (msg: \"Abrupt End TCP Server-" + suri_msg + "\"; " \
                            + "flowint: "+ tcpConvoCounterVarName+", isset; flags: R; " \
                            + " sid: " + str(suri_sid) + ";)"
                            suri_sid += 1
                            suricata_rule += "\r\n"
                            ####Reset Packet from Client
                            suricata_rule += "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                            + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                            + " (msg: \"Abrupt End TCP Client-" + suri_msg + "\"; " \
                            + "flowint: "+ tcpConvoCounterVarName+", isset; flags: R; " \
                            + " sid: " + str(suri_sid) + ";)"
                            suri_sid += 1
                            suricata_rule += "\r\n"
                            ####Conn Closed
                            suricata_rule += "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                            + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                            + " (msg: \"Conn Closed Gracefully-" + suri_msg + "\"; " \
                            + "flowint: "+ tcpConvoCounterVarName+", isset; flags: FA; " \
                            + " sid: " + str(suri_sid) + ";)"
                            suricata_rule += "\r\n"
                        else:
                            suricata_rule = "alert " + suri_proto + " " + suri_ip_src + " " + suri_sport + " " \
                            + suri_direction + " " + suri_ip_dest + " " + suri_dport \
                            + " (msg: \"" + suri_msg + "\"; " 
                            if suri_content != "":
                                suricata_rule += "content:" + suri_content + ";" 
                            suricata_rule += " flags: " + suri_flags + "; " + suri_custom_attr + " sid:" + str(suri_sid) + ";)"
                            
                logging.debug("Suricata Rule: \r\n")
                suricata_rules.append(suricata_rule)
            return suricata_rules
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("json_to_rules(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

    def write_rules_to_file(self, ofilename, ruledata):
        logging.debug("write_rules_to_file() Instantiated")
        try:
		    # now write output to a file
            logging.debug("write_rules_to_file() File opened for writing: " + str(ofilename))
            ruleOF = open(ofilename, "w")
            logging.debug("write_rules_to_file() Writing Rule Data to file.")
            for rule in ruledata:
                logging.debug("Rule: \r\n" + str(rule))
                ruleOF.write(str(rule) + "\r\n")
            logging.debug("write_rules_to_file() Writing complete; closing file.")
            ruleOF.close()
            logging.debug("write_rules_to_file() Completed.")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("write_rules_to_file(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

    def comply_string(self, mystring, replacePipe=False, replaceSemi=False):
        logging.debug("comply_string() Instantiated")
        if mystring == None or mystring == "":
            return ""
        answer = mystring
        if replacePipe:
            answer = answer.replace("|","|3A|")
        if replaceSemi:
            answer = answer.replace(";","|3B|")
        #These two are escaped in the JSON already, so I convert the escaped copies
        answer = answer.replace("\\n", "|0A|")
        answer = answer.replace("\\r", "|0D|")
        answer = answer.replace(":","|3A|")
        answer = answer.replace("\"","|22|")
        logging.debug("comply_string() compliant string: " + str(answer))        
        logging.debug("comply_string() Completed")        
        return answer

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.debug)
    logging.debug("Starting Program")
    if len(sys.argv) != 3:
        logging.error("Usage: suricata-rule-generator.py <path-to-comment-json> <output-path>")
        exit()
    ifilename = sys.argv[1]
    ofilename = sys.argv[2]
    se = SuricataRuleExtractor()
    ruledata = se.json_to_rules(ifilename)
    se.write_rules_to_file(ofilename, ruledata)
