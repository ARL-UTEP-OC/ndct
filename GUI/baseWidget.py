import logging
import sys
import os, traceback
import shutil
import time
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
                QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, 
                QSpinBox, QAction, qApp, QStackedWidget, QMenuBar)

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from LogManager import LogManager
from CommentManager.CommentManager import CommentManager
from Validator.Validator import Validator

from GUI.Dialogs.JSONFolderDialog import JSONFolderDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread
from GUI.MessageBoxes.ScoreMessageBox import ScoreMessageBox

class BaseWidget(QtWidgets.QWidget):
    def __init__(self, logman, comment_mgr, val):
        self.logger_started_once = False

        self.start_module = ConfigurationManager.get_instance().read_config_value("GUI","START_MODULE")

        QtWidgets.QWidget.__init__(self, parent=None)
        
        log_start_layout = QVBoxLayout()
        log_stop_layout = QVBoxLayout()
        wireshark_annotate_layout = QVBoxLayout()
        validate_layout = QHBoxLayout()

        self.setWindowTitle("BaseWidget")
        self.setObjectName("BaseWidget")
        layoutWidget = QtWidgets.QWidget()
        layoutWidget.setObjectName("layoutWidget")
        outerVertBox = QtWidgets.QVBoxLayout()
        outerVertBox.setObjectName("outerVertBox")
        layoutWidget.setLayout(outerVertBox)

        log_start_label = QLabel()
        log_start_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_start_label.setAlignment(Qt.AlignCenter)
        log_start_label.setText('Start Logging Network Data and Actions')
        log_start_layout.addWidget(log_start_label)

        self.log_start_button = QPushButton('Logger Start')
        self.log_start_button.clicked.connect(self.on_log_start_button_clicked)

        outerVertBox.addLayout(log_start_layout)

        log_stop_label = QLabel()
        log_stop_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_stop_label.setAlignment(Qt.AlignCenter)
        log_stop_label.setText('Stop Logging Network Data and Actions')
        log_stop_layout.addWidget(log_stop_label)

        self.log_stop_button = QPushButton('Logger Stop and Process')
        self.log_stop_button.clicked.connect(self.on_log_stop_button_clicked)
        self.log_stop_button.setEnabled(False)

        outerVertBox.addLayout(log_stop_layout)

        wireshark_annotate_label = QLabel()
        wireshark_annotate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        wireshark_annotate_label.setAlignment(Qt.AlignCenter)
        wireshark_annotate_label.setText('Use Wireshark to Add Comments to Logs')
        wireshark_annotate_layout.addWidget(wireshark_annotate_label)

        self.wireshark_annotate_button = QPushButton('Run Wireshark')
        self.wireshark_annotate_button.clicked.connect(self.on_wireshark_annotate_button_clicked)
        self.wireshark_annotate_button.setEnabled(False)

        outerVertBox.addLayout(wireshark_annotate_layout)

        validate_label = QLabel()
        validate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        validate_label.setAlignment(Qt.AlignCenter)
        validate_label.setText('Find Incidents in Another Network File Based on Comments')

        self.wireshark_file_button = QPushButton('Select File')
        self.wireshark_file_button.clicked.connect(self.on_wireshark_file_button_clicked)
        self.wireshark_file_button.setEnabled(False)

        self.wireshark_file_lineedit = QLineEdit()
        self.wireshark_file_lineedit.setText('Please select a pcap or pcapng file')
        self.wireshark_file_lineedit.setAlignment(Qt.AlignLeft)
        self.wireshark_file_lineedit.setReadOnly(True)
        self.wireshark_file_lineedit.setEnabled(False)

        self.validate_button = QPushButton('Find Incidents')
        self.validate_button.clicked.connect(self.on_validate_button_clicked)
        self.validate_button.setEnabled(False)

        log_start_layout.addWidget(self.log_start_button)
        log_stop_layout.addWidget(self.log_stop_button)
        wireshark_annotate_layout.addWidget(self.wireshark_annotate_button)

        validate_layout.addWidget(self.wireshark_file_button)
        validate_layout.addWidget(self.wireshark_file_lineedit)

        outerVertBox.addLayout(validate_layout)

        outerVertBox.addLayout(validate_layout)
        outerVertBox.addWidget(self.validate_button)
        outerVertBox.addStretch()

        paddingWidget1 = QtWidgets.QWidget()
        paddingWidget1.setObjectName("paddingWidget1")
        outerVertBox.addWidget(paddingWidget1)
        paddingWidget2 = QtWidgets.QWidget()
        paddingWidget2.setObjectName("paddingWidget2")
        outerVertBox.addWidget(paddingWidget2)
        paddingWidget3 = QtWidgets.QWidget()
        paddingWidget3.setObjectName("paddingWidget3")
        outerVertBox.addWidget(paddingWidget3)

        self.setLayout(outerVertBox)

        self.logman = logman
        self.comment_mgr = comment_mgr
        self.val = val

    def on_log_start_button_clicked(self):
        logging.debug('on_log_start_button_clicked(): Instantiated')
        if self.logger_started_once == True:
            buttonReply = QMessageBox.question(self, 'Confirmation', "Restarting the Logger will Remove any Previous Data. \r\n Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply != QMessageBox.Yes:
                logging.debug('on_log_start_button_clicked(): Cancelled')
                return
        self.logger_started_once = True
        self.logman.remove_data_all()
        self.logman.start_collectors()
        self.log_start_button.setEnabled(False)
        self.log_stop_button.setEnabled(True)
        self.wireshark_annotate_button.setEnabled(False)
        self.wireshark_file_button.setEnabled(False)
        self.wireshark_file_lineedit.setEnabled(False)
        self.validate_button.setEnabled(False)
        logging.debug('on_log_start_button_clicked(): Complete')

    def on_log_stop_button_clicked(self):
        logging.debug('on_log_stop_button_clicked(): Instantiated')

        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.stop_button_batch_completed)
        
        self.batch_thread.add_function(self.logman.stop_collectors)
        self.batch_thread.add_function(self.logman.parse_data_all)
        self.batch_thread.add_function(self.logman.export_data)
        self.batch_thread.add_function(self.logman.copy_latest_data)
        self.batch_thread.add_function(self.logman.generate_dissectors)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()
        
        logging.debug('on_log_stop_button_clicked(): Complete')

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def stop_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()

        output_dissected = "Processed Network Capture. \r\nIncludes:\r\n"
        for dissected in self.logman.get_generated_dissector_filenames():
            output_dissected += str(os.path.basename(dissected)) +"\r\n"

        if output_dissected == "":
            QMessageBox.alert(self, "Processing Complete", "No files processed")
        else: 
            QMessageBox.about(self, "Processing Complete", output_dissected)
            self.log_start_button.setEnabled(True)
            self.log_stop_button.setEnabled(False)
            self.wireshark_annotate_button.setEnabled(True)
            self.wireshark_file_button.setEnabled(False)
            self.wireshark_file_lineedit.setEnabled(False)
            self.validate_button.setEnabled(False)
        logging.debug('thread_finish(): Completed')

    def on_wireshark_annotate_button_clicked(self):
        logging.debug('on_activate_wireshark_button_clicked(): Instantiated')
        #open wireshark using the captured pcap and the generated lua files
        self.comment_mgr.run_wireshark_with_dissectors()
        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.wireshark_file_button.setEnabled(True)
        self.wireshark_file_lineedit.setEnabled(True)
        self.validate_button.setEnabled(False)
        logging.debug('on_activate_wireshark_button_clicked(): Complete')

    def on_wireshark_file_button_clicked(self):
        logging.debug('on_wireshark_file_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.debug("File choose canceled")
            return
        self.wireshark_file_lineedit.setText(file_chosen)
        if self.wireshark_file_lineedit.text() != "Please select a pcap or pcapng file":
            self.log_start_button.setEnabled(True)
            self.log_stop_button.setEnabled(False)
            self.wireshark_annotate_button.setEnabled(True)
            self.wireshark_file_button.setEnabled(True)
            self.wireshark_file_lineedit.setEnabled(True)
            self.validate_button.setEnabled(True)
        logging.debug('on_wireshark_file_button_clicked(): Complete')
    
    def on_validate_button_clicked(self):
        logging.debug('on_validate_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.validate_button_batch_completed)
        
        self.batch_thread.add_function( self.comment_mgr.extract_json)
        self.batch_thread.add_function( self.comment_mgr.extract_json)
        self.batch_thread.add_function( self.comment_mgr.write_comment_json_to_file)

        self.batch_thread.add_function( self.val.extract_rules)
        self.batch_thread.add_function( self.val.write_rules_to_file)

        self.batch_thread.add_function( self.val.run_suricata_with_rules, None, None, None, None, self.wireshark_file_lineedit.text())
        self.batch_thread.add_function( self.val.generate_score_report)
        #self.val.write_score_file()

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        logging.debug('on_validate_button_clicked(): Complete')

    def validate_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')

        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        #get score report
        
        smb = ScoreMessageBox(self.val.get_score_report())
        smb.exec_()

        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.wireshark_file_button.setEnabled(True)
        self.wireshark_file_lineedit.setEnabled(True)
        self.validate_button.setEnabled(True)

        logging.debug('thread_finish(): Completed')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = BaseWidget()
    ui.show()
    sys.exit(app.exec_())