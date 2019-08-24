import logging
import subprocess
import shlex
import sys
import os
from PyQt5.QtCore import QThread
from CommentManager.CommentExtractor import CommentExtractor
from CommentManager.WiresharkRunner import WiresharkRunner
from ConfigurationManager.ConfigurationManager import ConfigurationManager

class CommentManager():

    def __init__(self, user_pcap_filename = None):
        logging.debug('CommentManager(): Instantiated')
        self.user_pcap_filename = user_pcap_filename
        if user_pcap_filename == None:
            #read from config file
            self.commented_pcap_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "USER_PCAP_FILENAME")
        
        self.ce = CommentExtractor()
        logging.debug('CommentManager(): Complete')

    def extractJSON(self):
        logging.debug('extractJSON(): Instantiated')
        self.jsondata = self.ce.commentToJSON(self.commented_pcap_filename)
        logging.debug('extractJSON(): Completed')
    
    def writeCommentJSONToFile(self, comment_json_output_filename = None):
        logging.debug('writeCommentJSONToFile(): Instantiated')
        self.comment_json_output_filename = comment_json_output_filename
        if self.comment_json_output_filename == None:
            #read from config file
            self.comment_json_output_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "COMMENTS_JSON_FILENAME")
        self.ce.writeJSONToFile(self.comment_json_output_filename, self.jsondata)
        logging.debug('writeCommentJSONToFile(): Completed')

    def run_wireshark_with_dissectors(self, dissector_filenames=[], user_pcap_filename=None):
        logging.debug('run_wireshark_with_dissectors(): Instantiated')

        self.user_pcap_filename = user_pcap_filename
        if user_pcap_filename == None:
            #read from config file
            self.user_pcap_filename = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER", "USER_PCAP_FILENAME")

        self.wireshark_thread = WiresharkRunner(lua_scripts=dissector_filenames, pcap_filename=self.user_pcap_filename)
        self.wireshark_thread.start()
        logging.debug('run_wireshark_with_dissectors(): Instantiated')
