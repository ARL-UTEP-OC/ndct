from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import os
import sys, traceback
import logging
import shutil
from pathlib import Path

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from GUI.Threading.BatchThread import BatchThread
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

class ResultsWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel, resultsDir, val):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.resultsDir = resultsDir
        self.val = val

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBoxAnnot")

        self.setWindowTitle("ResultsWidget")
        self.setObjectName("ResultsWidget")

        #Label - Results Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.resultLabel = QtWidgets.QLabel("RESULTS")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.resultLabel.setFont(labelFont)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxSess.addWidget(self.resultLabel)

        #get project-session rules path
        projectpath = os.path.join(projectfolder, projectName)
        projectPCAPFolder = os.path.join(projectpath, "PCAP/")
        sessionPCAPFolder = os.path.join(projectPCAPFolder, sessionLabel)
        self.sessionPCAP = os.path.join(sessionPCAPFolder, "NeedsAnnotation.pcapng")

        #Create dir for session alerts
        self.sessionAlertsDir = os.path.join(resultsDir, sessionLabel)

        try:
            if os.path.exists(self.sessionAlertsDir):
                shutil.rmtree(self.sessionAlertsDir, ignore_errors=True)
            os.makedirs(self.sessionAlertsDir)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("comment_to_json(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        #get session rules
        self.sessionRulesDir = os.path.join(projectpath, "RULES")
        self.sessionRulesDir = os.path.join(self.sessionRulesDir, sessionLabel)
        self.rules_filename = os.path.join(self.sessionRulesDir, ConfigurationManager.STRUCTURE_RULES_GEN_FILE)

        #Path to where the rules stored
        self.ruleHorBox = QtWidgets.QHBoxLayout()
        self.ruleHorBox.setObjectName("ruleHorBox")
        self.rulePathLabel = QtWidgets.QLabel()
        self.rulePathLabel.setObjectName("rulePathLabel")
        self.rulePathLabel.setText("Rule Path: ")
        self.ruleHorBox.addWidget(self.rulePathLabel)

        self.ruleLineEdit = QtWidgets.QLineEdit()
        self.ruleLineEdit.setAcceptDrops(False)
        self.ruleLineEdit.setReadOnly(True)
        self.ruleLineEdit.setObjectName("ruleLineEdit")
        self.ruleLineEdit.setText(self.sessionRulesDir)
        self.ruleLineEdit.setAlignment(Qt.AlignLeft)
        self.ruleHorBox.addWidget(self.ruleLineEdit)

        self.rulePathViewButton = QPushButton("View")
        self.rulePathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.sessionRulesDir))
        self.ruleHorBox.addWidget(self.rulePathViewButton)

        #Annotated/Suspect PCAP
        self.pcapHorBox2 = QtWidgets.QHBoxLayout()
        self.pcapHorBox2.setObjectName("pcapHorBox2")
        self.pcapLabel2 = QtWidgets.QLabel()
        self.pcapLabel2.setObjectName("pcapLabel2")
        self.pcapLabel2.setText("Apply Rules to PCAP:  ")
        self.pcapHorBox2.addWidget(self.pcapLabel2)

        self.pcapLineEdit2 = QtWidgets.QLineEdit()
        self.pcapLineEdit2.setFixedWidth(150)
        #self.pcapLineEdit2.setFixedHeight(25)
        self.pcapLineEdit2.setAcceptDrops(False)
        self.pcapLineEdit2.setReadOnly(True)
        self.pcapLineEdit2.setObjectName("pcapLineEdit2") 
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox2.addWidget(self.pcapLineEdit2)
        
        #view and ... button
        self.suspViewButton = QPushButton("View")
        self.suspPathButton = QPushButton("...")
        self.pcapHorBox2.addWidget(self.suspPathButton)
        self.pcapHorBox2.addWidget(self.suspViewButton)

        #on buttons clicked
        self.suspViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.pcapLineEdit2))
        self.suspPathButton.clicked.connect(self.on_path_button_clicked)

        #Show path to the alert folder
        self.alertHorBox = QtWidgets.QHBoxLayout()
        self.alertHorBox.setObjectName("alertHorBox")
        self.alertPathLabel = QtWidgets.QLabel()
        self.alertPathLabel.setObjectName("alertPathLabel")
        self.alertPathLabel.setText("Alert Output Path: ")
        self.alertHorBox.addWidget(self.alertPathLabel)

        self.alertLineEdit = QtWidgets.QLineEdit()
        self.alertLineEdit.setAcceptDrops(False)
        self.alertLineEdit.setReadOnly(True)
        self.alertLineEdit.setObjectName("alertLineEdit")
        self.alertLineEdit.setText(self.sessionAlertsDir)
        self.alertLineEdit.setAlignment(Qt.AlignLeft)
        self.alertHorBox.addWidget(self.alertLineEdit)

        self.alertPathViewButton = QPushButton("View")
        self.alertPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.sessionAlertsDir))
        self.alertHorBox.addWidget(self.alertPathViewButton)

        #Generate Alerts Button
        self.alertButtonHorBox = QtWidgets.QHBoxLayout()
        self.alertButtonHorBox.setObjectName("alertButtonHorBox")
        self.alertButton = QPushButton("Generate Alerts")
        self.alertButton.setEnabled(False)
        self.alertButton.clicked.connect(self.on_alert_button_clicked)
        self.alertButtonHorBox.setAlignment(Qt.AlignRight)
        self.alertButtonHorBox.addWidget(self.alertButton)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.ruleHorBox)
        self.outerVertBox.addLayout(self.pcapHorBox2)
        self.outerVertBox.addLayout(self.alertHorBox)
        self.outerVertBox.addLayout(self.alertButtonHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        elif isinstance(folder_path, QtWidgets.QLineEdit):
            folder_path = folder_path.text()
        if folder_path == "":
            QMessageBox.warning(self, 
                                "No path selected",
                                "There is no path selected",
                                QMessageBox.Ok)
            return None

        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

    def on_alert_button_clicked(self):
        logging.debug('on_analyze_out_start_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.analyze_button_batch_completed)
        alertOutPath = os.path.join(self.sessionAlertsDir)
        try:
            if os.path.exists(alertOutPath):
                shutil.rmtree(self.sessionAlertsDir, ignore_errors=True)
            os.makedirs(alertOutPath)
        except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error("comment_to_json(): An error occured ")
                traceback.print_exception(exc_type, exc_value, exc_traceback)

        suricata_config_filename = ConfigurationManager.get_instance().read_config_abspath("VALIDATOR", "SURICATA_CONFIG_FILENAME")
        self.batch_thread.add_function( self.val.run_suricata_with_rules, None, suricata_config_filename, alertOutPath, self.rules_filename, self.pcapLineEdit2.text())
        logging.debug("SUSPECT PCAP: " + self.pcapLineEdit2.text())

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        logging.debug('on_analyze_out_start_button_clicked(): Complete')

    def analyze_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')

        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        alertOutFile = os.path.join(self.sessionAlertsDir, ConfigurationManager.STRUCTURE_ALERT_GEN_FILE)
        if os.path.exists(alertOutFile) == False or os.stat(alertOutFile).st_size < 10:
            QMessageBox.about(self, "IDS Alerts", "No alerts generated")
        else:
            res = QMessageBox.question(self,
                                            "Alerts written.\r\n",
                                            "Open File?",
                                            QMessageBox.Yes | QMessageBox.No)
            
            if res == QMessageBox.Yes:
                logging.debug("analyze_button_batch_completed(): Opening Alerts File")
                self.on_view_button_clicked(None, alertOutFile)
    
    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def on_path_button_clicked(self):
        logging.debug('on_path_button_clicked(): Instantiated')
        choose_file = QFileDialog()
        filenames, _ = QFileDialog.getOpenFileNames(choose_file, "Select Suspect File")
        if len(filenames) < 0:
            logging.debug("File choose cancelled")
            return
        
        if len(filenames) > 0:
            suspect_pcap_chosen = filenames[0]
            session_pcaps = os.path.dirname(os.path.abspath(self.sessionPCAP))
            self.suspect_pcap_path = os.path.join(session_pcaps, "SuspectPCAP.pcapng")
            self.batch_thread = BatchThread()
            self.batch_thread.progress_signal.connect(self.update_progress_bar)
            self.batch_thread.completion_signal.connect(self.copy_suspect_complete)
            self.batch_thread.add_function(self.copy_file, suspect_pcap_chosen, self.suspect_pcap_path)
            #shutil.copy(suspect_pcap_chosen, suspect_pcap_path)

            self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
            self.batch_thread.start()
            self.progress_dialog_overall.show()

        logging.debug('on_path_button_clicked(): Complete')

    def copy_file(self, file, dst):
        shutil.copy(file, dst)

    def copy_suspect_complete(self):
        self.pcapLineEdit2.setText(self.suspect_pcap_path)
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        self.alertButton.setEnabled(True)


