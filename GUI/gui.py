import sys
import logging
import os, traceback
import shutil
import platform
from PyQt5 import QtGui, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, QSpinBox, QTextEdit, QAction, qApp, QFileDialog, QMessageBox

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from LogManager import LogManager
from CommentManager.CommentManager import CommentManager
from Validator.Validator import Validator

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from GUI.Dialogs.JSONFolderDialog import JSONFolderDialog
from GUI.Dialogs.WiresharkFileDialog import WiresharkFileDialog
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread
from GUI.MessageBoxes.ScoreMessageBox import ScoreMessageBox

import time

class MainGUI(QMainWindow):
    def __init__(self, logman, comment_mgr, val):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__()

        uic.loadUi('GUI/eceld-netsys.ui', self)
        
        self.start_module = ConfigurationManager.get_instance().read_config_value("GUI","START_MODULE")

        self.logger_started_once = False

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        ## Collect Tab Items
        self.logOutPathButton.clicked.connect(self.on_log_out_path_button_clicked)
        self.logOutPathButton.setEnabled(True)
        self.logOutViewButton.clicked.connect(lambda x: self.on_log_out_view_button_clicked(x, self.logOutPathEdit))
        self.logOutViewButton.setEnabled(False)

        self.logOutStartButton.clicked.connect(self.on_log_start_button_clicked)
        self.logOutStartButton.setEnabled(False)
        self.logOutStopButton.clicked.connect(self.on_log_stop_button_clicked)
        self.logOutStopButton.setEnabled(False)
        
        ## Annotate Tab Items
        self.annotateOutStartButton.clicked.connect(self.on_wireshark_annotate_button_clicked)
        self.annotateOutStartButton.setEnabled(False)

        self.pcapInPathButton.clicked.connect(self.on_wireshark_file_button_clicked)
        self.pcapInPathButton.setEnabled(False)

        # self.analyzeOutStartButton.clicked.connect(self.on_validate_button_clicked)
        self.analyzeOutStartButton.setEnabled(False)

        if self.start_module == "COMMENT_MANAGER":
            self.collectTab.setEnabled(False)
        if self.start_module == "VALIDATOR":
            self.collectTab.setEnabled(False)
            self.annotateOutStartButton.setEnabled(False)

        self.logman = logman
        self.comment_mgr = comment_mgr
        self.val = val

        logging.debug("MainWindow(): Complete")

    def on_log_out_path_button_clicked(self):
        logging.debug('on_log_out_path_button_clicked(): Instantiated')
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder_chosen == "":
            logging.debug("File choose canceled")
            return
        self.logOutPathEdit.setText(folder_chosen)

        if self.logOutPathEdit.toPlainText() != "":
            self.logOutStartButton.setEnabled(True)
            self.logOutStopButton.setEnabled(False)
            self.annotateOutStartButton.setEnabled(True)
            self.pcapInPathButton.setEnabled(True)
            self.pcapInEdit.setEnabled(True)
            self.logOutViewButton.setEnabled(True)
        logging.debug('on_log_out_path_button_clicked(): Complete')

    def on_log_out_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

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
        self.logOutStartButton.setEnabled(False)
        self.logOutStopButton.setEnabled(True)
        self.annotateOutStartButton.setEnabled(False)
        self.pcapInPathButton.setEnabled(False)
        self.pcapInEdit.setEnabled(False)
        # self.validate_button.setEnabled(False)
        logging.debug('on_log_start_button_clicked(): Complete')

    def on_log_stop_button_clicked(self):
        logging.debug('on_log_stop_button_clicked(): Instantiated')

        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.stop_button_batch_completed)
        
        self.batch_thread.add_function(self.logman.stop_collectors)
        self.batch_thread.add_function(self.logman.parse_data_all)
        self.batch_thread.add_function(self.logman.export_data, self.logOutPathEdit.toPlainText())
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

        output_dissected = "Saved Logs. \r\n\r\nCreated:\r\n"
        for dissected in self.logman.get_generated_dissector_filenames():
            output_dissected += str(os.path.basename(dissected)) +"\r\n"

        if output_dissected == "":
            QMessageBox.alert(self, "Processing Complete", "No files processed")
        else: 
            QMessageBox.about(self, "Processing Complete", output_dissected)
            self.logOutStartButton.setEnabled(True)
            self.logOutStopButton.setEnabled(False)
            self.annotateOutStartButton.setEnabled(True)
            self.pcapInPathButton.setEnabled(False)
            self.pcapInEdit.setEnabled(False)
            self.logInPathEdit.setText(self.logOutPathEdit.toPlainText())
            # self.validate_button.setEnabled(False)
        logging.debug('thread_finish(): Completed')

    def on_wireshark_annotate_button_clicked(self):
        logging.debug('on_activate_wireshark_button_clicked(): Instantiated')
        #open wireshark using the captured pcap and the generated lua files
        self.comment_mgr.run_wireshark_with_dissectors()
        self.logOutStartButton.setEnabled(True)
        self.logOutStopButton.setEnabled(False)
        self.annotateOutStartButton.setEnabled(True)
        self.pcapInPathButton.setEnabled(True)
        self.pcapInEdit.setEnabled(True)
        # self.validate_button.setEnabled(False)
        logging.debug('on_activate_wireshark_button_clicked(): Complete')

    def on_wireshark_file_button_clicked(self):
        logging.debug('on_wireshark_file_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.debug("File choose canceled")
            return
        self.pcapInEdit.setText(file_chosen)
        if self.pcapInEdit.text() != "Please select a pcap or pcapng file":
            self.logOutStartButton.setEnabled(True)
            self.logOutStopButton.setEnabled(False)
            self.annotateOutStartButton.setEnabled(True)
            self.pcapInPathButton.setEnabled(True)
            self.pcapInEdit.setEnabled(True)
            # self.validate_button.setEnabled(True)
        logging.debug('on_wireshark_file_button_clicked(): Complete')
    
    def on_validate_button_clicked(self):
        logging.debug('on_validate_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        # self.batch_thread.completion_signal.connect(self.validate_button_batch_completed)
        
        self.batch_thread.add_function( self.comment_mgr.extract_json)
        self.batch_thread.add_function( self.comment_mgr.extract_json)
        self.batch_thread.add_function( self.comment_mgr.write_comment_json_to_file)

        self.batch_thread.add_function( self.val.extract_rules)
        self.batch_thread.add_function( self.val.write_rules_to_file)

        self.batch_thread.add_function( self.val.run_suricata_with_rules, None, None, None, None, self.pcapInEdit.text())
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

        self.logOutStartButton.setEnabled(True)
        self.logOutStopButton.setEnabled(False)
        self.annotateOutStartButton.setEnabled(True)
        self.pcapInPathButton.setEnabled(True)
        self.pcapInEdit.setEnabled(True)
        # self.validate_button.setEnabled(True)

        logging.debug('thread_finish(): Completed')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        if self.logOutStartButton.isEnabled() == True:
            self.quit_app()
        if self.logOutStartButton.isEnabled() == False:
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


    def quit_app(self):
        logging.debug("quit_app(): Instantiated()")
        self.destroy()
        self.quit_event.accept()
        qApp.quit()
        logging.debug("quit_app(): Completed()")
        return