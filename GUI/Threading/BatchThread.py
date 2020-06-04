import logging
import os
from PyQt5.QtCore import QThread, pyqtSignal
import time

class BatchThread(QThread):
    progress_signal = pyqtSignal()
    completion_signal = pyqtSignal()

    def __init__(self):
        logging.debug('BatchThread(): Instantiated')
        QThread.__init__(self)
        self.functionlist = []
        logging.debug('BatchThread(): Completed')

    def add_function(self, funcname, *args):
        logging.debug('BatchThread.add_function(): Instantiated')
        self.functionlist.append((funcname, *args))
        logging.debug('BatchThread.add_function(): Complete')

    def get_load_count(self):
        return len(self.functionlist)
    
    def run(self):
        logging.debug('BatchThread.run(): Instantiated')
        
        for ((funcname, *args)) in self.functionlist:
            #run the function with provided arguments
            funcname(*args)
            #emit when file done reading
            self.progress_signal.emit()
        self.completion_signal.emit()
        logging.debug('BatchThread.run(): Completed')