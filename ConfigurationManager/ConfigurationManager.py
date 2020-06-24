import logging
import configparser
import os
import sys, traceback

class ConfigurationManager():
    __instance = None
    
    CONFIG_FILENAME = "config.ini"
    STRUCTURE_PARSED_PATH="ParsedLogs"
    STRUCTURE_ANNOTATED_PCAP_FILE=os.path.join("PCAP", "AnnotatedPCAP.pcapng")
    STRUCTURE_GEN_DISSECTORS_PATH="GeneratedDissectors"
    STRUCTURE_JSON_COMMENTS=os.path.join("tmp", "comments.JSON")
    STRUCTURE_RULES_GEN_FILE=os.path.join("GeneratedRules","generated.rules")
    STRUCTURE_ALERT_GEN_PATH=os.path.join("IDS-ALERTS")
    STRUCTURE_ALERT_GEN_FILE=os.path.join("IDS-ALERTS","fast.log")

    @staticmethod 
    def get_instance():
        logging.debug('ConfigurationManager(): Singleton Instantiated')
        if ConfigurationManager.__instance == None:
            ConfigurationManager()
        return ConfigurationManager.__instance

    def __init__(self):
        logging.debug('ConfigurationManager(): Single inner class Instantiated')
        if ConfigurationManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            logging.debug('ConfigurationManager(): Instantiated')
        
            self.cp = configparser.ConfigParser()
            try:
                self.cp.read(ConfigurationManager.CONFIG_FILENAME)

            except:
                logging.error("exportData(): An error occured when trying to read config file: " + str(ConfigurationManager.CONFIG_FILENAME))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

            logging.debug('ConfigurationManager(): Completed Instantiation')
            ConfigurationManager.__instance = self

    def read_config_abspath(self, configsection, configkey):
        logging.debug('readConfigValue(): Instantiated')
        if configsection in self.cp and configkey in self.cp[configsection]:
            return os.path.abspath(self.cp[configsection][configkey])
        else:
            logging.error("ConfigurationManager(): section/key not found in config file: " + os.path.abspath(ConfigurationManager.CONFIG_FILENAME) + " " + str(configsection) + "/" + str(configkey))
        return None

    def read_config_value(self, configsection, configkey):
        logging.debug('readConfigValue(): Instantiated')
        if configsection in self.cp and configkey in self.cp[configsection]:
            return self.cp[configsection][configkey]
        else:
            logging.error("ConfigurationManager(): section/key not found in config file: " + os.path.abspath(ConfigurationManager.CONFIG_FILENAME) + " " + str(configsection) + "/" + str(configkey))
        return None

    def set_config_file(self, config_filename):
        try:
            self.cp.read(config_filename)
        except:
            logging.error("exportData(): An error occured when trying to read config file: " + str(ConfigurationManager.CONFIG_FILENAME))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Instantiating ConfigurationManager()")
    cm = ConfigurationManager.get_instance()
    cm2 = ConfigurationManager.get_instance()
    logging.debug("Checking Key/Values")
    logging.debug(cm2.read_config_abspath("GUI", "SHOW_COLLECTION_WIDGETS"))
    logging.debug(cm2.read_config_abspath("GUI", "NOT_HERE"))
    logging.debug(cm2.read_config_abspath("NOT_HERE", "NOT_HERE"))
    logging.debug("Completed ConfigurationManager()") 


