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
from GUI.Dialogs.RulesFileDialog import RulesFileDialog
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
        self.logOutViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.logOutPathEdit))
        self.logOutViewButton.setEnabled(False)
        self.logOutStartButton.clicked.connect(self.on_log_start_button_clicked)
        self.logOutStartButton.setEnabled(False)
        self.logOutStopButton.clicked.connect(self.on_log_stop_button_clicked)
        self.logOutStopButton.setEnabled(False)
        
        ## Annotate Tab Items
        self.logInPathButton.clicked.connect(self.on_log_in_path_button_clicked)
        self.logInPathButton.setEnabled(True)
        self.logInViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.logInEdit))
        self.logInViewButton.setEnabled(False)
        self.annotateOutStartButton.clicked.connect(self.on_select_annotate_file_button_clicked)
        self.annotateOutStartButton.setEnabled(False)

        
        ## Gen Rules Tab Items
        self.annotateInPathButton.clicked.connect(self.on_annotate_in_path_button_clicked)
        self.annotateInViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.annotateInEdit))
        self.annotateInViewButton.setEnabled(False)
        self.genRulesOutPathButton.clicked.connect(self.on_genrules_out_path_button_clicked)
        self.genRulesOutViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.genRulesOutEdit))
        self.genRulesOutViewButton.setEnabled(False)
        self.genRulesOutStartButton.clicked.connect(self.on_genrules_out_start_button_clicked)
        self.genRulesOutStartButton.setEnabled(False)


        ## Analyze Tab Items
        self.genRulesInPathButton.clicked.connect(self.on_genrules_in_path_button_clicked)
        self.genRulesInViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.genRulesInEdit))
        self.genRulesInViewButton.setEnabled(False)
        self.pcapInPathButton.clicked.connect(self.on_pcap_in_path_button_clicked)
        self.pcapInViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.pcapInEdit))
        self.pcapInViewButton.setEnabled(False)      
        self.alertOutPathButton.clicked.connect(self.on_alert_out_path_button_clicked)
        self.alertOutViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.alertOutEdit))
        self.alertOutViewButton.setEnabled(False)
        self.analyzeOutStartButton.clicked.connect(self.on_analyze_out_start_button_clicked)
        self.analyzeOutStartButton.setEnabled(False)
        

        ## Enable certain tabs based on configuration
        if self.start_module == "COMMENT_MANAGER":
            self.collectTab.setEnabled(False)
        if self.start_module == "VALIDATOR":
            self.collectTab.setEnabled(False)
            self.annotateOutStartButton.setEnabled(False)

        ## Instantiate managers
        self.logman = logman
        self.comment_mgr = comment_mgr
        self.val = val

        logging.debug("MainWindow(): Complete")

###### Non-specific Events
    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

###### Collect Tab Events
    def on_log_out_path_button_clicked(self):
        logging.debug('on_log_out_path_button_clicked(): Instantiated')
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Store Data"))
        if folder_chosen == "":
            logging.debug("File choose cancelled")
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
        self.annotateTab.setEnabled(False)
        self.generateRulesTab.setEnabled(False)
        self.analyzeTab.setEnabled(False)

        self.logOutPathButton.setEnabled(False)
        self.logOutViewButton.setEnabled(False)
        self.logOutStartButton.setEnabled(False)
        self.logOutStopButton.setEnabled(True)
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
        parsedLogs = os.path.join(self.logOutPathEdit.toPlainText(),ConfigurationManager.STRUCTURE_PARSED_PATH)
        annotatedPCAP = os.path.join(self.logOutPathEdit.toPlainText(), ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
        self.batch_thread.add_function(self.logman.copy_latest_data, self.logOutPathEdit.toPlainText(), parsedLogs, annotatedPCAP)
        dissectorsPath = os.path.join(self.logOutPathEdit.toPlainText(), ConfigurationManager.STRUCTURE_GEN_DISSECTORS_PATH)
        self.batch_thread.add_function(self.logman.generate_dissectors, parsedLogs, dissectorsPath, None)

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
            self.annotateTab.setEnabled(True)
            self.generateRulesTab.setEnabled(True)
            self.analyzeTab.setEnabled(True)
            self.logOutStartButton.setEnabled(True)
            self.logOutStopButton.setEnabled(False)
            self.logOutPathButton.setEnabled(True)
            self.logOutViewButton.setEnabled(True)
            annotatedPCAP = os.path.join(self.logOutPathEdit.toPlainText(), ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
            self.logInEdit.setText(annotatedPCAP)
            self.logInViewButton.setEnabled(True)
            self.annotateOutStartButton.setEnabled(True)
            self.tabWidget.setCurrentIndex(1)
            
        logging.debug('thread_finish(): Completed')

##### Annotate Tab Events
    def on_log_in_path_button_clicked(self):
        logging.debug('on_log_in_path_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.debug("File choose canceled")
            return
        self.logInEdit.setText(file_chosen)
        if self.logInEdit.toPlainText() != "":
            self.logInViewButton.setEnabled(True)
        self.annotateOutStartButton.setEnabled(True)
        logging.debug('on_log_in_path_button_clicked(): Complete')

    def on_select_annotate_file_button_clicked(self):
        logging.debug('on_select_annotate_file_button_clicked(): Instantiated')
        #open wireshark using pcap and provide base so that the dissectors can be found
        user_pcap_filename = self.logInEdit.toPlainText()
        pcapBasepath = os.path.dirname(os.path.dirname(self.logInEdit.toPlainText()))
        dissectorsPath = os.path.join(pcapBasepath, ConfigurationManager.STRUCTURE_GEN_DISSECTORS_PATH)
        if os.path.exists(dissectorsPath):
            self.comment_mgr.run_wireshark_with_dissectors(pcapBasepath, user_pcap_filename)
        else:
            self.comment_mgr.run_wireshark_with_dissectors([], self.logInEdit.toPlainText())
        self.annotateOutStartButton.setEnabled(True)
        self.annotateInEdit.setText(user_pcap_filename)
        self.annotateInViewButton.setEnabled(True)
        if self.genRulesOutViewButton.isEnabled():
            self.genRulesOutStartButton.setEnabled(True)
        logging.debug('on_select_annotate_file_button_clicked(): Complete')

##### GenRules Tab Events
    def on_annotate_in_path_button_clicked(self):
        logging.debug('on_annotate_in_path_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.debug("File choose canceled")
            return
        self.annotateInEdit.setText(file_chosen)
        if self.annotateInEdit.toPlainText() != "":
            self.annotateInViewButton.setEnabled(True)
        if self.genRulesOutViewButton.isEnabled():
            self.genRulesOutStartButton.setEnabled(True)
        logging.debug('on_log_in_path_button_clicked(): Complete')

    def on_genrules_out_path_button_clicked(self):
        logging.debug('on_genrules_out_path_button_clicked(): Instantiated')
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Folder to Save IDS Rules"))
        if folder_chosen == "":
            logging.debug("File choose cancelled")
            return
        self.genRulesOutEdit.setText(folder_chosen)

        if self.genRulesOutEdit.toPlainText() != "":
            self.genRulesOutViewButton.setEnabled(True)
        if self.annotateInViewButton.isEnabled():
            self.genRulesOutStartButton.setEnabled(True)
        logging.debug('on_log_in_path_button_clicked(): Complete')

    def on_genrules_out_start_button_clicked(self):
        logging.debug('on_genrules_out_start_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.genrules_button_batch_completed)

        self.batch_thread.add_function( self.comment_mgr.extract_json, self.annotateInEdit.toPlainText())
        comment_filename = os.path.join(self.genRulesOutEdit.toPlainText(), ConfigurationManager.STRUCTURE_JSON_COMMENTS)
        self.batch_thread.add_function( self.comment_mgr.write_comment_json_to_file, comment_filename)

        self.batch_thread.add_function( self.val.extract_rules, comment_filename)
        rules_filename = os.path.join(self.genRulesOutEdit.toPlainText(), ConfigurationManager.STRUCTURE_RULES_GEN_FILE)
        self.batch_thread.add_function( self.val.write_rules_to_file, rules_filename)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        logging.debug('on_genrules_out_start_button_clicked(): Complete')

    def genrules_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')

        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        rules_filename = os.path.join(self.genRulesOutEdit.toPlainText(), ConfigurationManager.STRUCTURE_RULES_GEN_FILE)
        self.genRulesInEdit.setText(rules_filename)
        self.genRulesInViewButton.setEnabled(True)
        self.tabWidget.setCurrentIndex(3)
        logging.debug('thread_finish(): Completed')

##### Analyze Tab Events
    def on_genrules_in_path_button_clicked(self):
        logging.debug('on_genrules_in_path_button_clicked(): Instantiated')
        file_chosen = RulesFileDialog().rules_dialog()
        if file_chosen == "":
            logging.debug("File choose canceled")
            return
        self.genRulesInEdit.setText(file_chosen)

        if self.genRulesInEdit.toPlainText() != "":
            self.genRulesInViewButton.setEnabled(True)
        if self.pcapInViewButton.isEnabled() and self.alertOutViewButton.isEnabled():
            self.analyzeOutStartButton.setEnabled(True)
        logging.debug('on_genrules_in_path_button_clicked(): Complete')

    def on_pcap_in_path_button_clicked(self):
        logging.debug('on_pcap_in_path_button_clicked(): Instantiated')
        file_chosen = WiresharkFileDialog().wireshark_dialog()
        if file_chosen == "":
            logging.debug("File choose cancelled")
            return
        self.pcapInEdit.setText(file_chosen)
        if self.pcapInEdit.toPlainText() != "":
            self.pcapInViewButton.setEnabled(True)
        if self.genRulesInViewButton.isEnabled() and self.alertOutViewButton.isEnabled():
            self.analyzeOutStartButton.setEnabled(True)
        logging.debug('on_pcap_in_path_button_clicked(): Complete')

    def on_alert_out_path_button_clicked(self):
        logging.debug('on_alert_out_path_button_clicked(): Instantiated')
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Folder to Save IDS Output/Alerts"))
        if folder_chosen == "":
            logging.debug("File choose cancelled")
            return
        self.alertOutEdit.setText(folder_chosen)

        if self.alertOutEdit.toPlainText() != "":
            self.alertOutViewButton.setEnabled(True)
        if self.genRulesInViewButton.isEnabled() and self.pcapInViewButton.isEnabled():
            self.analyzeOutStartButton.setEnabled(True)
        logging.debug('on_alert_out_path_button_clicked(): Complete')

    def on_analyze_out_start_button_clicked(self):
        logging.debug('on_analyze_out_start_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.analyze_button_batch_completed)
#run_suricata_with_rules(self, suricata_executable_filename=None, suricata_config_filename=None, suricata_alert_path=None, suricata_rules_filename=None, validate_pcap_filename=None):
        alertOutPath = os.path.join(self.alertOutEdit.toPlainText(), ConfigurationManager.STRUCTURE_ALERT_GEN_PATH)
        self.batch_thread.add_function( self.val.run_suricata_with_rules, None, None, alertOutPath, self.genRulesInEdit.toPlainText(), self.pcapInEdit.toPlainText())
        #self.batch_thread.add_function( self.val.generate_score_report)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        logging.debug('on_analyze_out_start_button_clicked(): Complete')

    def analyze_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')

        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        
        res = QMessageBox.question(self,
                                        "Alerts written.\r\n",
                                        "Open File?",
                                        QMessageBox.Yes | QMessageBox.No)
        alertOutFile = os.path.join(self.alertOutEdit.toPlainText(), ConfigurationManager.STRUCTURE_ALERT_GEN_FILE)
        if res == QMessageBox.Yes:
            logging.debug("analyze_button_batch_completed(): Opening Alerts File")
            self.on_view_button_clicked(None, alertOutFile)
    
    # def on_validate_button_clicked(self):
    #     logging.debug('on_validate_button_clicked(): Instantiated')
        
    #     self.batch_thread = BatchThread()
    #     self.batch_thread.progress_signal.connect(self.update_progress_bar)
    #     # self.batch_thread.completion_signal.connect(self.validate_button_batch_completed)
        
    #     self.batch_thread.add_function( self.comment_mgr.extract_json)
    #     self.batch_thread.add_function( self.comment_mgr.write_comment_json_to_file)

    #     self.batch_thread.add_function( self.val.extract_rules)
    #     self.batch_thread.add_function( self.val.write_rules_to_file)

    #     self.batch_thread.add_function( self.val.run_suricata_with_rules, None, None, None, None, self.pcapInEdit.text())
    #     self.batch_thread.add_function( self.val.generate_score_report)
    #     #self.val.write_score_file()

    #     self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
    #     self.batch_thread.start()
    #     self.progress_dialog_overall.show()

    #     logging.debug('on_validate_button_clicked(): Complete')

    # def validate_button_batch_completed(self):
    #     logging.debug('thread_finish(): Instantiated')

    #     self.progress_dialog_overall.update_progress()
    #     self.progress_dialog_overall.hide()
    #     #get score report
        
    #     smb = ScoreMessageBox(self.val.get_score_report())
    #     smb.exec_()

    #     self.logOutStartButton.setEnabled(True)
    #     self.logOutStopButton.setEnabled(False)
    #     self.annotateOutStartButton.setEnabled(True)
    #     self.pcapInPathButton.setEnabled(True)
    #     self.pcapInEdit.setEnabled(True)
    #     # self.validate_button.setEnabled(True)

    #     logging.debug('thread_finish(): Completed')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        if self.logOutStopButton.isEnabled() == False:
            self.quit_app()
        if self.logOutStopButton.isEnabled() == True:
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