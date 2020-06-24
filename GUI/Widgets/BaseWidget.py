import logging
import sys
import os, traceback
import shutil
import time
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
                QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, 
                QSpinBox, QAction, qApp, QStackedWidget, QMenuBar, QMessageBox)

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread


class BaseWidget(QtWidgets.QWidget):
    def __init__(self):
        self.logger_started_once = False

        self.start_module = ConfigurationManager.get_instance().read_config_value("GUI","START_MODULE")

        QtWidgets.QWidget.__init__(self, parent=None)
        
        self.setWindowTitle("BaseWidget")
        self.setObjectName("BaseWidget")
        layoutWidget = QtWidgets.QWidget()
        layoutWidget.setObjectName("layoutWidget")
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")
        layoutWidget.setLayout(self.outerVertBox)

        self.setLayout(self.outerVertBox)
    
    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        if self.log_start_button.isEnabled() == True:
            self.quit_app()
        if self.log_start_button.isEnabled() == False:
            close = QMessageBox.question(self,
                                            "QUIT",
                                            "Logger is running. Stop and Quit?",
                                            QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                logging.debug("closeEvent(): Creating Quit Command Load")
                self.batch_thread = BatchThread()
                self.batch_thread.progress_signal.connect(self.update_progress_bar)
                self.batch_thread.completion_signal.connect(self.quit_app)
                
                self.batch_thread.add_function(self.logman.stop_collectors)
                self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
                self.batch_thread.start()
                self.progress_dialog_overall.show()
                return
        logging.debug("closeEvent(): returning ignore")
        event.ignore()
        return
