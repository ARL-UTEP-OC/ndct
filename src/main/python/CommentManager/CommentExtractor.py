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

class CommentExtractor():

	TSHARK_COMMAND = "tshark"

	def __init__(self):
		pass

	def commentToJSON(self, ifilename):
		logging.debug("commentToJSON() Instantiated.")
		try:
			#TODO add default -edata field
			extract_cmd = CommentExtractor.TSHARK_COMMAND + " -r " + ifilename + " -T fields  -E separator=, -eframe.protocols -eframe.time_epoch -eframe.number -eip.src -eip.dst -eudp.srcport -eudp.dstport -etcp.srcport -etcp.dstport -etcp.flags.str -etcp.payload -eframe.comment pkt_comment"
			#extractCmd = tsharkCommand + " -r " + inputFilename + " -T fields" + " -E separator=," + " -eframe.protocols" + " -eframe.time_epoch" + " -eip.src" + " -eip.dst" + " -eudp.srcport" + " -eudp.dstport" + " -etcp.srcport" + " -etcp.dstport" + " -etcp.flags")
			logging.debug("commentToJSON() running command: " + extract_cmd)
			process = Popen(shlex.split(extract_cmd), stdout=subprocess.PIPE)
			logging.debug("commentToJSON() waiting for system call to complete...")
			out, err = process.communicate()
			logging.debug("commentToJSON() Completed.")
			return self.procOutputToJSON(out)
			
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logging.error("commentToJSON(): An error occured ")
			traceback.print_exception(exc_type, exc_value, exc_traceback)
			exit()		
	
	def procOutputToJSON(self, outdata):
		logging.debug("procOutputToJSON() Instantiated")
		id = 0
		comment_data_list = []
		logging.debug("procOutputToJSON() Reading Packet Data")
		for field in outdata.splitlines():
			id+=1
			protocol_dict = {}

			#parse out data into packet-related info and packet comment related info
			field = str(field, encoding="utf-8")
			packet_info = field.split(",")[:11]
			(protocols, time_epoch, number, ip_src, ip_dst, udp_srcport, udp_dstport, tcp_srcport, tcp_dstport, tcp_flags, tcp_payload) = packet_info
			packet_comment = field.split(",")[11]
			if "**" not in packet_comment:
				logging.error( "packet_comment malformatted; skipping: " + str(packet_comment))
				exit()
			scope = payload_identifier = sf_call = description = confidence = ""
			#check what fields are non-empty#
			fields = packet_comment.split("**")
			for field in fields:
				if field.startswith("scope="):
					if len(field.split("=")) > 0:
						scope = field.split("=")[1]
				elif field.startswith("important-packet-identifier="):
					if len(field.split("=")) > 0:
						payload_identifier = field.split("=")[1]
				elif field.startswith("cmd="):
					if len(field.split("=")) > 0:
						sf_call = field.split("=")[1]
				elif field.startswith("description="):
					if len(field.split("=")) > 0:
						description = field.split("=")[1]
				elif field.startswith("confidence"):
					if len(field.split("=")) > 0:
						confidence = field.split("=")[1]

			#now fill in any that are required with default values:
			if scope == "":
				scope = "single"
			if payload_identifier == "":
				payload_identifier = ""
			logging.debug("procOutputToJSON(): packet_info: " + str(packet_info))
			logging.debug("procOutputToJSON(): packet_comment: " + str(packet_comment))
			
			#build basic IP json:
			if "eth:ethertype:ip" in protocols: 
				#hard coded keep values for now
				ip_src_dict = {"val": ip_src, "keep": "false"}
				ip_dest_dict = {"val": ip_dst, "keep": "true"}
				comm_mode_dict = None

				if scope == "single":
					#hard coded direction for now
					direction_dict = {"direction": ">"}
					comm_mode_dict = {"single": direction_dict}
				elif scope == "conversation":
					comm_mode_dict = "conversation"
				elif scope.startswith("suricata;"):
					logging.debug("procOutputToJSON(): Suricata " + str(scope))
					comm_mode_dict = {"suricata-rule-attr": scope.split(";")[1:]}
				elif scope == "filter":
					pass
				elif scope == "packet-range":
					pass	

				protocol_dict["eth:ethertype:ip"] = {"ip_src": ip_src_dict, "ip_dest": ip_dest_dict, "comm_mode": comm_mode_dict}
			
				#build additional details specific to ICMP
				if "eth:ethertype:ip:icmp" in protocols:
					#Need to enable default payload using -edata in tshark above
					#if payload_identifier == "all-packet-payload":
					#	mypayload = payload
					#else: 
					#	mypayload = payload_identifier
					mypayload = ""
					payload_identifier_dict = {"payload": mypayload, "casematters": "", "type": "ignore"}
					protocol_dict["eth:ethertype:ip:icmp"] = {"payload-identifier": payload_identifier_dict}

				#build additional details specific to TCP
				if "eth:ethertype:ip:tcp" in protocols:
					#TODO
					#hard coded keep values for now; may be hard for participants with no prior network skills
					sport_dict = {"val": tcp_srcport, "keep": "false"}
					dport_dict = {"val": tcp_dstport, "keep": "false"}

					#TODO payload-based identification for TCP 
					#let user choose if case matters
					
					if payload_identifier == "all-packet-payload":
						payload_type = "all"
						mypayload = tcp_payload
					elif payload_identifier == "":
						payload_type = "ignore"
						mypayload = ""
					else:
						payload_type = "match"
						mypayload = payload_identifier

					payload_identifier_dict = {"type": payload_type, "payload": mypayload, "casematters": "true"}

					protocol_dict["eth:ethertype:ip:tcp"] = {"sport": sport_dict, "dport": dport_dict, "flags": tcp_flags, "payload-identifier": payload_identifier_dict}
			
			logging.debug("procOutputToJSON(): Done Reading Packet Data")

			#build the over-arching comment_data object
			comment_data_list.append({"id": id, "frameno": number, "protocol": protocol_dict, "description": description, "run-descriptor": sf_call})
			logging.debug("procOutputToJSON(): Formatted JSON:"+json.dumps(comment_data_list, indent=3))
			logging.debug("procOutputToJSON() Completed.")

		return comment_data_list
			
	def writeJSONToFile(self, ofilename, jsonData):
		logging.debug("writeJSONToFile() Instantiated")
		try:
			# now write output to a file
			logging.debug("writeJSONToFile() File opened for writing: " + str(ofilename))
			#first create the directory if it doesn't exist yet:
			dirname = os.path.dirname(ofilename)
			if os.path.exists(dirname) == False:
				os.makedirs(dirname)
			jsonOF = open(ofilename, "w")
			logging.debug("writeJSONToFile() Writing JSON Data to file.")
			jsonOF.write(json.dumps(jsonData, indent=3, sort_keys=True))
			logging.debug("writeJSONToFile() Writing complete; closing file.")
			jsonOF.close()
			logging.debug("writeJSONToFile() Completed.")
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			logging.error("writeJSONToFile(): An error occured")
			traceback.print_exception(exc_type, exc_value, exc_traceback)
			exit()

if __name__ == "__main__":
	logging.getLogger().setLevel(logging.DEBUG)
	logging.debug("Starting Program")
	if len(sys.argv) != 3:
		logging.error("Usage: CommentExtractor.py <path-to-pcapng> <output-path>")
		exit()
	ifilename = sys.argv[1]
	ofilename = sys.argv[2]
	ce = CommentExtractor()
	jsondata = ce.commentToJSON(ifilename)
	ce.writeJSONToFile(ofilename, jsondata)
