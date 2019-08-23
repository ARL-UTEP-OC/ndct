import logging
import os
from PyQt5.QtCore import QThread, pyqtSignal
import time

class BatchThread(QThread):
    signal = pyqtSignal()
    signal2 = pyqtSignal()

    def __init__(self):
        logging.debug('BatchThread(): Instantiated')
        QThread.__init__(self)
        self.functionlist = []
        logging.debug('BatchThread(): Completed')

    def addFunction(self, funcname, *args):
        logging.debug('BatchThread.addFunction(): Instantiated')
        self.functionlist.append((funcname, *args))
        logging.debug('BatchThread.addFunction(): Complete')

    def getLoadCount(self):
        return len(self.functionlist)
    
    def run(self):
        logging.debug('BatchThread.run(): Instantiated')
        
        for ((funcname, *args)) in self.functionlist:
            #run the function with provided arguments
            funcname(*args)
            #emit when file done reading
            self.signal.emit()
        self.signal2.emit()
        logging.debug('BatchThread.run(): Completed')