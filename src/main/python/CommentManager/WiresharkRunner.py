import logging
import subprocess
import shlex
import sys
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from PyQt5.QtCore import QThread

class WiresharkRunner(QThread):

    def __init__(self, lua_scripts=None, pcap_filename=None):
        logging.debug('WiresharkRunner(): Instantiated')
        QThread.__init__(self)
        self.cmd = ConfigurationManager.get_instance().read_config_abspath("COMMENT_MANAGER","WIRESHARK_FILENAME")
        if pcap_filename != None:
            self.cmd+= " -r " + pcap_filename
        if lua_scripts != None and len(lua_scripts) > 0:
            for lua_script in lua_scripts:
                self.cmd+= " -Xlua_script:" + lua_script
        logging.debug('WiresharkRunner(): Complete')

    def run(self):
        logging.debug('WiresharkRunner.run(): Instantiated')
        if sys.platform == "linux" or sys.platform == "linux2":
            output = subprocess.check_output(shlex.split(self.cmd), encoding="utf-8")
        else: 
            output = subprocess.check_output(self.cmd, encoding="utf-8")

        logging.debug('WiresharkRunner.run(): Complete')

