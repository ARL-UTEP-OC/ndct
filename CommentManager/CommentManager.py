import logging
import subprocess
import shlex
import sys, traceback
import os
from PyQt5.QtCore import QThread
from CommentManager.CommentExtractor import CommentExtractor
from CommentManager.WiresharkRunner import WiresharkRunner
from ConfigurationManager.ConfigurationManager import ConfigurationManager

class CommentManager():

    def __init__(self, path_for_latest_pcap = None):
        logging.debug('CommentManager(): Instantiated')
        self.path_for_latest_pcap = path_for_latest_pcap
        if path_for_latest_pcap == None:
            #read from config file
            self.commented_pcap_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "PATH_FOR_LATEST_PCAP")
        
        self.ce = CommentExtractor()
        logging.debug('CommentManager(): Complete')

    def extract_json(self, commented_pcap_filename = None):
        logging.debug('extract_json(): Instantiated')
        self.commented_pcap_filename = commented_pcap_filename
        if commented_pcap_filename == None:
            self.commented_pcap_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "PATH_FOR_LATEST_PCAP")
        self.jsondata = self.ce.comment_to_json(self.commented_pcap_filename)
        logging.debug('extract_json(): Completed')
    
    def write_comment_json_to_file(self, comment_json_output_filename = None):
        logging.debug('write_comment_json_to_file(): Instantiated')
        self.comment_json_output_filename = comment_json_output_filename
        if self.comment_json_output_filename == None:
            #read from config file
            self.comment_json_output_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "COMMENTS_JSON_FILENAME")
        self.ce.write_json_to_file(self.comment_json_output_filename, self.jsondata)
        logging.debug('write_comment_json_to_file(): Completed')

    def run_wireshark_with_dissectors(self, dissector_path=[], path_for_latest_pcap=None):
        logging.debug('run_wireshark_with_dissectors(): Instantiated')

        self.path_for_latest_pcap = path_for_latest_pcap
        filelist = list()

        if path_for_latest_pcap == None:
            #read from config file
            self.path_for_latest_pcap = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "PATH_FOR_LATEST_PCAP")
        self.dissector_path = dissector_path
        if dissector_path == []:
            #read from config file
            self.dissector_path = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "DISSECTOR_PATH")
        if os.path.exists(self.dissector_path):
            #get dissector filenames in path
            try:
                logging.debug("run_wireshark_with_dissectors(): reading dissector filenames")
                print("Iterating: " + str(self.dissector_path))
                for r, d, f in os.walk(self.dissector_path):
                    for file in f:
                        if '.lua' in file:
                            filelist.append(os.path.join(r, file))

            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error("read_json_data(): An error occured ")
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                exit()	   

        if len(filelist) == 0:
            self.wireshark_thread = WiresharkRunner(pcap_filename=self.path_for_latest_pcap)
        else:
            self.wireshark_thread = WiresharkRunner(lua_scripts=filelist, pcap_filename=self.path_for_latest_pcap)
        self.wireshark_thread.start()
        logging.debug('run_wireshark_with_dissectors(): Completed')
