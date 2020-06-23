from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QTextEdit, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import logging
import os

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread

class NewProjectDialog(QtWidgets.QWidget):
    def __init__(self, logman):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.logger_started_once = False

        self.existingconfignames = []

        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("New Project")
        self.setObjectName("NewProjectDialog")

        self.nameVerBoxPro = QtWidgets.QHBoxLayout()
        self.nameVerBoxPro.setObjectName("nameVerBoxPro")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Type in New Project Name:")
        self.nameVerBoxPro.addWidget(self.nameLabel)
        self.configname = QtWidgets.QLineEdit()

        #Create buttons for creating new file
        self.pathLabel = QtWidgets.QLabel()
        self.pathLabel.setObjectName("pathLabel")
        self.pathLabel.setText("Select Directory to Save Project:")
        self.logOutPathEdit = QTextEdit()
        self.logOutPathEdit.setObjectName("logOutPathEdit")
        self.logOutPathEdit.setAlignment(Qt.AlignLeft)
        ######
        self.logOutPathEdit.setGeometry(QtCore.QRect(169,20,256,27))
        ######
        self.logOutPathButton = QPushButton("...")
        self.logOutViewButton = QPushButton("View")
        self.logOutStartButton = QPushButton("Start Logging")
        self.logOutStopButton = QPushButton("Stop Logging")
        self.logOutSaveButton = QPushButton("Save/Create")
        self.logOutCancelButton = QPushButton("Cancel")

        #Add on click event
        self.logOutPathButton.clicked.connect(self.on_log_out_path_button_clicked)
        self.logOutPathButton.setEnabled(True)
        self.logOutViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.logOutPathEdit))
        self.logOutViewButton.setEnabled(False)
        self.logOutStartButton.clicked.connect(self.on_log_start_button_clicked)
        self.logOutStartButton.setEnabled(False)
        self.logOutStopButton.clicked.connect(self.on_log_stop_button_clicked)
        self.logOutStopButton.setEnabled(False)
        self.logOutSaveButton.clicked.connect(self.on_log_save_button_clicked)
        self.logOutSaveButton.setEnabled(False)

        #Set the button layouts
        self.pathLabel_layout = QtWidgets.QVBoxLayout()
        self.pathEdit_layout = QtWidgets.QHBoxLayout()
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #Put all the components together
        self.nameVerBoxPro.addWidget(self.configname)
        self.pathLabel_layout.addWidget(self.pathLabel)
        self.pathEdit_layout.addWidget(self.logOutPathEdit)
        self.pathEdit_layout.addWidget(self.logOutPathButton)
        self.pathEdit_layout.addWidget(self.logOutViewButton)
        self.bottomButtons_layout.addWidget(self.logOutStartButton)
        self.bottomButtons_layout.addWidget(self.logOutStopButton)
        self.bottomButtons_layout.addWidget(self.logOutSaveButton)
        self.bottomButtons_layout.addWidget(self.logOutCancelButton, alignment=QtCore.Qt.AlignRight)
        
        self.outerVertBoxPro.addLayout(self.nameVerBoxPro)
        self.outerVertBoxPro.addLayout(self.pathLabel_layout)
        self.outerVertBoxPro.addLayout(self.pathEdit_layout)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.paddingWidget1 = QtWidgets.QWidget()
        self.paddingWidget1.setObjectName("paddingWidget1")
        self.outerVertBoxPro.addWidget(self.paddingWidget1)
        self.paddingWidget2 = QtWidgets.QWidget()
        self.paddingWidget2.setObjectName("paddingWidget2")
        self.outerVertBoxPro.addWidget(self.paddingWidget2)
        self.paddingWidget3 = QtWidgets.QWidget()
        self.paddingWidget3.setObjectName("paddingWidget3")
        self.outerVertBoxPro.addWidget(self.paddingWidget3)

        self.setLayout(self.outerVertBoxPro)

        self.logman = logman

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

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

        self.logOutSaveButton.setEnabled(True)
        
        logging.debug('on_log_stop_button_clicked(): Complete')

    def on_log_save_button_clicked(self):
        logging.debug('on_log_save_button_clicked(): Instantiated')

        if self.configname != '':
            self.configname = ''.join(e for e in self.configname if e.isalnum())
            if self.configname in self.existingconfignames:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "The project name specified already exists",
                                        QMessageBox.Ok)            
                return None
            else:
                #if all good, add to existing file names list
                self.existingconfignames += [self.configname]
        else:
             QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Type in a name for the New Project",
                                        QMessageBox.Ok)

        logging.debug('on_log_save_button_clicked(): Complete')