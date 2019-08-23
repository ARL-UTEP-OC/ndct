import logging
import sys
import os, traceback
import shutil
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox, QAction, qApp

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from LogManager import LogManager
from CommentManager.CommentManager import CommentManager
from Validator.Validator import Validator

from GUI.Dialogs.JSONFolderDialog import JSONFolderDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread
from GUI.MessageBoxes.ScoreMessageBox import ScoreMessageBox


import time

from PyQt5.QtWidgets import QMessageBox

class MainApp(QMainWindow):

    def __init__(self):
        logging.debug("MainApp(): Instantiated")
        super(MainApp, self).__init__()
        self.logger_started_once = False
        self.setWindowTitle('Traffic Annotation Workflow')

        mainwidget = QWidget()
        self.setCentralWidget(mainwidget)
        mainlayout = QVBoxLayout()
        log_start_layout = QHBoxLayout()
        log_stop_layout = QHBoxLayout()
        wireshark_annotate_layout = QHBoxLayout()
        validate_layout = QHBoxLayout()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        log_start_label = QLabel('Step I. Start Logging Network Data and Actions')
        log_start_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_start_label.setAlignment(Qt.AlignCenter)

        self.log_start_button = QPushButton('Logger Start')
        self.log_start_button.clicked.connect(self.on_log_start_button_clicked)

        log_stop_label = QLabel('Step II. Stop Logging Network Data and Actions')
        log_stop_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        log_stop_label.setAlignment(Qt.AlignCenter)

        self.log_stop_button = QPushButton('Logger Stop and Process')
        self.log_stop_button.clicked.connect(self.on_log_stop_button_clicked)
        self.log_stop_button.setEnabled(False)

        wireshark_annotate_label = QLabel('Step III. Use Wireshark to Add Comments to Logs')
        wireshark_annotate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        wireshark_annotate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_annotate_button = QPushButton('Run Wireshark')
        self.wireshark_annotate_button.clicked.connect(self.on_wireshark_annotate_button_clicked)
        self.wireshark_annotate_button.setEnabled(False)

        validate_label = QLabel('Step IV. Find Incidents in Another Network File Based on Comments')
        validate_label.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
        validate_label.setAlignment(Qt.AlignCenter)

        self.wireshark_file_button = QPushButton('Select File')
        self.wireshark_file_button.clicked.connect(self.on_wireshark_file_button_clicked)
        self.wireshark_file_button.setEnabled(True)

        self.wireshark_file_lineedit = QLineEdit()
        self.wireshark_file_lineedit.setText('Please select a pcap or pcapng file')
        self.wireshark_file_lineedit.setAlignment(Qt.AlignLeft)
        self.wireshark_file_lineedit.setReadOnly(True)
        self.wireshark_file_lineedit.setEnabled(True)

        self.validate_button = QPushButton('Find Incidents')
        self.validate_button.clicked.connect(self.on_validate_button_clicked)
        self.validate_button.setEnabled(True)

        log_start_layout.addWidget(self.log_start_button)
        log_stop_layout.addWidget(self.log_stop_button)
        wireshark_annotate_layout.addWidget(self.wireshark_annotate_button)

        validate_layout.addWidget(self.wireshark_file_button)
        validate_layout.addWidget(self.wireshark_file_lineedit)
        
        mainlayout.addWidget(log_start_label)
        mainlayout.addLayout(log_start_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(log_stop_label)
        mainlayout.addLayout(log_stop_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(wireshark_annotate_label)
        mainlayout.addLayout(wireshark_annotate_layout)
        mainlayout.addStretch()
        mainlayout.addWidget(validate_label)
        mainlayout.addLayout(validate_layout)
        mainlayout.addWidget(self.validate_button)
        mainlayout.addStretch()
        mainwidget.setLayout(mainlayout)

        self.logman = LogManager.LogManager()
        self.comment_mgr = CommentManager()
        self.val = Validator()

        logging.debug("MainWindow(): Complete")
    
    def on_log_start_button_clicked(self):
        logging.debug('on_log_start_button_clicked(): Instantiated')
        if self.logger_started_once == True:
            buttonReply = QMessageBox.question(self, 'Confirmation', "Restarting the Logger will Remove any Previous Data. \r\n Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply != QMessageBox.Yes:
                logging.debug('on_log_start_button_clicked(): Cancelled')
                return
        self.logger_started_once = True
        self.logman.removeDataAll()
        self.logman.startCollectors()
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
        self.batch_thread.signal.connect(self.update_progress_bar)
        self.batch_thread.signal2.connect(self.thread_finish)
        
        self.batch_thread.addFunction(self.logman.stopCollectors)
        self.batch_thread.addFunction(self.logman.parseDataAll)
        self.batch_thread.addFunction(self.logman.exportData)
        self.batch_thread.addFunction(self.logman.copyLatestData)
        self.batch_thread.addFunction(self.logman.generateDissectors)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.getLoadCount())
        self.batch_thread.start()
        self.progress_dialog_overall.show()
        
        logging.debug('on_log_stop_button_clicked(): Complete')

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def thread_finish(self):
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
        self.comment_mgr.run_wireshark_with_dissectors(self.logman.get_generated_dissector_filenames())
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
            logging.error("File choose canceled")
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
        self.comment_mgr.extractJSON()
        self.comment_mgr.writeCommentJSONToFile()

        self.val.extract_rules()
        self.val.writeRulesToFile()
        self.val.run_suricata_with_rules()
        score_data = self.val.generate_score_report()
        smb = ScoreMessageBox(score_data)
        smb.exec_()
        #self.val.write_score_file()

        self.log_start_button.setEnabled(True)
        self.log_stop_button.setEnabled(False)
        self.wireshark_annotate_button.setEnabled(True)
        self.wireshark_file_button.setEnabled(True)
        self.wireshark_file_lineedit.setEnabled(True)
        self.validate_button.setEnabled(True)
        logging.debug('on_validate_button_clicked(): Complete')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        if self.log_start_button.isEnabled() == True:
            self.quitApp()
        if self.log_start_button.isEnabled() == False:
            close = QMessageBox.question(self,
                                            "QUIT",
                                            "Logger is running. Stop and Quit?",
                                            QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                logging.debug("closeEvent(): Creating Quit Command Load")
                self.batch_thread = BatchThread()
                self.batch_thread.signal.connect(self.update_progress_bar)
                self.batch_thread.signal2.connect(self.quitApp)
                
                self.batch_thread.addFunction(self.logman.stopCollectors)
                self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.getLoadCount())
                self.batch_thread.start()
                self.progress_dialog_overall.show()
                return
        logging.debug("closeEvent(): returning ignore")
        event.ignore()
        return
    
    def quitApp(self):
        logging.debug("quitApp(): Instantiated()")
        self.destroy()
        self.quit_event.accept()
        qApp.quit()
        logging.debug("quitApp(): Completed()")
        return

if __name__ == '__main__':
    logging.debug("main(): Instantiated")
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    appctxt = ApplicationContext()
    app = MainApp()
    app.setGeometry(500, 300, 500, 150)
    app.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    logging.debug("main(): Complete")