import time
import logging
import os
import sys, traceback
from subprocess import Popen
import Pyro4

class ECELDClient():
    def __init__(self):
        logging.debug("Instantiating ecel_manager()")
        #start the nameserver
        logging.debug("ecel_manager(): attempting to start the pyro name server")

        logging.debug("ecel_manager(): getting a handle to the ecel.service")
        self.ecel_manager = Pyro4.Proxy("PYRONAME:ecel.service")    # use name server object lookup uri shortcut

    def start_collectors(self):
        logging.debug("start_collectors(): requesting to remove all data")
        self.ecel_manager.remove_data()
        logging.debug("start_collectors(): requesting to start collectors")
        self.ecel_manager.start_collectors()

    def stop_collectors(self):
        logging.debug("stop_collectors(): requesting to stop collectors")
        self.ecel_manager.stop_collectors()

    def parse_data_all(self):
        logging.debug("parse_data_all(): requesting to parse all data")
        self.ecel_manager.parse_data_all()
        time.sleep(5)

    def export_data(self, path=None):
        logging.debug("export_data(): requesting to export data to " + str(path))
        if path == None:
            path = "/tmp/"
        try:
            if os.path.exists(path) == False:
                logging.debug("export_data(): requesting to export data to " + str(path))
                os.makedirs(path)
        except:
            logging.error("export_data(): An error occured when trying to use path for export: " + str(path))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        self.ecel_manager.export_data(path)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Instantiating ECELDClient()")
    eclient = ECELDClient()
    eclient.start_collectors()
    time.sleep(5)
    eclient.stop_collectors()
    eclient.parse_data_all()
    eclient.export_data(path="/root/Desktop/")
    logging.debug("Completed ECELDClient()") 
