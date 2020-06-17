import logging
import sys
import os, traceback
import shutil
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox, QAction, qApp

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from LogManager.LogManager import LogManager
from CommentManager.CommentManager import CommentManager
from Validator.Validator import Validator

from GUI.gui import MainGUI

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    logging.debug("MainApp(): Starting GUI")
    logging.debug("MainApp(): Instantiating LogManager")
    logman = LogManager()
    logging.debug("MainApp(): Instantiating Comment Manager")
    comment_mgr = CommentManager()
    logging.debug("MainApp(): Instantiating Validator")
    validator = Validator()

    if len(sys.argv) > 2:
        if os.path.exists(sys.argv[1]):
            logging.debug("MainApp(): Setting up configuration manager")
            ConfigurationManager.get_instance().set_config_file(sys.argv[1])
        else:
            logging.debug("MainApp(): config file " + sys.argv[1] + " does not exist")
    
    logging.debug("MainApp(): Instantiated")
    logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(message)s', level = logging.DEBUG)

    appctxt = QApplication(sys.argv)
    gui = MainGUI(logman, comment_mgr, validator)
    gui.setGeometry(500, 300, 500, 100)
    gui.show()
    exit_code = appctxt.exec_()
    sys.exit(exit_code)
    logging.debug("MainApp(): Complete")

