import logging
import subprocess
import shlex
import sys
import os
import shutil
import sys, traceback
from PyQt5.QtCore import QThread
from Validator.SuricataRuleExtractor import SuricataRuleExtractor
from Validator.Scorer import Scorer
from ConfigurationManager.ConfigurationManager import ConfigurationManager

class Validator():
    ALERT_FILENAME = "fast.log"
    def __init__(self, commented_json_filename = None):
        logging.debug('CommentManager(): Instantiated')
        #will likely use the GUI Threading here for this; from the GUI, however      
        self.se = SuricataRuleExtractor()
        self.scorer = Scorer()
        self.commented_json_filename = commented_json_filename
        if self.commented_json_filename == None:
            #read from config file
            self.commented_json_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "COMMENTS_JSON_FILENAME")

        logging.debug('CommentManager(): Complete')

    def extract_rules(self, commented_json_filename=None):
        logging.debug('extract_json(): Instantiated')
        self.commented_json_filename = commented_json_filename
        if self.commented_json_filename == None:
            #read from config file
            self.commented_json_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "COMMENTS_JSON_FILENAME")
        self.rule_list = self.se.json_to_rules(self.commented_json_filename)
        logging.debug('extract_json(): Completed')

    def write_rules_to_file(self, rules_output_filename = None):
        logging.debug('write_rules_to_file(): Instantiated')
        self.rules_output_filename = rules_output_filename
        if rules_output_filename == None:
            #read from config file
            self.rules_output_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_RULES_FILENAME")
        try:
            #make sure path exists, if not, create it
            dirname = os.path.dirname(self.rules_output_filename)
            if os.path.exists(dirname) == False:
                os.makedirs(dirname)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("write_rules_to_file(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

        self.se.write_rules_to_file(self.rules_output_filename, self.rule_list)
        logging.debug('write_rules_to_file(): Completed')

    def run_suricata_with_rules(self, suricata_executable_filename=None, suricata_config_filename=None, suricata_alert_path=None, suricata_rules_filename=None, validate_pcap_filename=None):
        logging.debug('run_suricata_with_rules(): Instantiated')
        ##Read configuration from the setup file##
        self.suricata_executable_filename = suricata_executable_filename
        if self.suricata_executable_filename == None:
            #read from config file
            self.suricata_executable_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_EXECUTABLE_FILENAME")

        self.suricata_config_filename = suricata_config_filename
        if self.suricata_config_filename == None:
            #read from config file
            self.suricata_config_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_CONFIG_FILENAME")

        self.suricata_alert_path = suricata_alert_path
        if self.suricata_alert_path == None:
            #read from config file
            self.suricata_alert_path = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_ALERT_PATH")
        try:
            #if path exists, remove it and then recreate it
            if os.path.exists(self.suricata_alert_path) == True:
                shutil.rmtree(self.suricata_alert_path, ignore_errors=True)
            os.makedirs(self.suricata_alert_path)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("write_rules_to_file(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

        self.suricata_rules_filename = suricata_rules_filename
        if self.suricata_rules_filename == None:
            #read from config file
            self.suricata_rules_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_RULES_FILENAME")

        self.validate_pcap_filename = validate_pcap_filename
        if self.validate_pcap_filename == None:
            #read from config file
            self.validate_pcap_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "PCAP_FOR_VALIDATION_FILENAME")

        #Sample command: suricata -c /etc/suricata/suricata.yaml -l . -r $1 -k none
        logging.debug('run_suricata_with_rules(): Instantiated')
        self.cmd = self.suricata_executable_filename
        self.cmd+= " -c " + self.suricata_config_filename
        self.cmd+= " -l " + self.suricata_alert_path
        self.cmd+= " -r " + self.validate_pcap_filename
        self.cmd+= " -s " + self.suricata_rules_filename
        self.cmd+= " -k none"

        if sys.platform == "linux" or sys.platform == "linux2":
            logging.debug('run_suricata_with_rules(): Running Command: ' + str(self.cmd))
            output = subprocess.check_output(shlex.split(self.cmd))
        else: 
            logging.debug('run_suricata_with_rules(): Running Command: ' + str(self.cmd))
            output = subprocess.check_output(self.cmd)
        logging.debug('run_suricata_with_rules(): Complete')

    def generate_score_report(self, suricata_soln_alerts_json=None, suricata_alert_path=None):
        logging.debug('generate_score_report(): Instantiated')
        self.suricata_soln_alerts_json = suricata_soln_alerts_json
        if self.suricata_soln_alerts_json == None:
            #read from config file
            self.suricata_soln_alerts_json = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SOLN_FILENAME")
        self.suricata_alert_path = suricata_alert_path
        if self.suricata_alert_path == None:
            #read from config file
            self.suricata_alert_path = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_ALERT_PATH")
        #generate the scoring bin data structure based on the input JSON data 
        self.scorer.extract_solutions_from_json(self.suricata_soln_alerts_json)
        #generate the report:
        self.scorer.score_alerts(os.path.join(self.suricata_alert_path,Validator.ALERT_FILENAME))
        self.score_data = self.scorer.generate_results_report()
        logging.debug('generate_score_report(): Completed')

    def get_score_report(self):
        logging.debug('get_score_report(): Instantiated')
        logging.debug('get_score_report(): Completed')
        return self.scorer.get_score_report()
        
    def write_score_file(self, oscore_file=None):
        logging.debug('write_score_file(): Instantiated')
        self.oscore_file = oscore_file
        if self.oscore_file == None:
            self.oscore_file = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SCORE_REPORT_FILENAME")
        self.scorer.write_results_to_file(self.oscore_file, self.score_data)
        logging.debug('write_score_file(): Completed')