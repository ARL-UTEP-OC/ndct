from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QTextEdit, QMessageBox, QSizePolicy, QAction, qApp, QLabel, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QKeyEvent, QTextCursor
import logging
import os
import sys, traceback
import shutil
import re

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread

class NewFromPCAPDialog(QtWidgets.QWidget):
    #Signal for when the user is done creating the new project
    created = QtCore.pyqtSignal(str, dict, str)
    def __init__(self, existingProjects):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.logger_started_once = False

        self.existingconfignames = existingProjects
        self.projectPath = ""
        self.projectName = ""
        self.cancel_pressed = False
        self.saved_pressed = False
        self.cm = ConfigurationManager.get_instance()
        self.project_data_folder = self.cm.read_config_value("PROJECTS", "PROJECTS_BASE_PATH")

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("Project from PCAP")
        self.setObjectName("NewFromPCAP")

        #Label - New Project Title
        self.labelVerBoxPro = QtWidgets.QVBoxLayout()
        self.labelVerBoxPro.setObjectName("labeVerBoxPro")
        self.newProjectLabel = QLabel("Create Project from PCAP")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.newProjectLabel.setFont(labelFont)
        self.newProjectLabel.setAlignment(Qt.AlignCenter)

        self.projectNameHorBoxPro = QtWidgets.QHBoxLayout()
        self.projectNameHorBoxPro.setObjectName("projectNameHorBoxPro")
        self.projectNameLabel = QtWidgets.QLabel()
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.projectNameLabel.setText("Type in New Project Name:")
        self.projectNameHorBoxPro.addWidget(self.projectNameLabel)
        self.configname = QLineEdit()
        self.configname.textChanged.connect(self.on_configname_changed)
        self.configname.setFixedHeight(27)
        self.projectNameHorBoxPro.addWidget(self.configname)

        self.pcapNameHorBoxPro = QtWidgets.QHBoxLayout()
        self.pcapNameHorBoxPro.setObjectName("pcapNameHorBoxPro")
        self.pcapNameLabel = QtWidgets.QLabel()
        self.pcapNameLabel.setObjectName("pcapNameLabel")
        self.pcapNameLabel.setText("Path to PCAP:")
        self.pcapNameHorBoxPro.addWidget(self.pcapNameLabel)
        self.pcapNameLineEdit = QLineEdit()
        self.pcapNameLineEdit.setEnabled(False)
        self.pcapNameLineEdit.setFixedHeight(27)
        self.pcapNameHorBoxPro.addWidget(self.pcapNameLineEdit)
        self.selectPCAPButton = QPushButton("...")
        self.selectPCAPButton.clicked.connect(self.on_select_PCAP_button_clicked)
        self.pcapNameHorBoxPro.addWidget(self.selectPCAPButton)

        #Create buttons for OK/Cancel
        self.okButton = QPushButton("OK")
        self.okButton.setEnabled(False)
        self.okButton.clicked.connect(self.on_ok_button_clicked)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #Put all the components together
        self.labelVerBoxPro.addWidget(self.newProjectLabel)
        self.bottomButtons_layout.addWidget(self.okButton)
        self.bottomButtons_layout.addWidget(self.cancelButton, alignment=QtCore.Qt.AlignRight)
        
        self.outerVertBoxPro.addLayout(self.labelVerBoxPro)
        self.outerVertBoxPro.addLayout(self.projectNameHorBoxPro)
        self.outerVertBoxPro.addLayout(self.pcapNameHorBoxPro)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.setLayout(self.outerVertBoxPro)
    
    def on_configname_changed(self):
        #logging.debug('on_configname_changed(): Instantiated')
        if self.pcapNameLineEdit.text() != "" and self.configname.text() != "":
            self.okButton.setEnabled(True)
        else:
            self.okButton.setEnabled(False)

    def on_select_PCAP_button_clicked(self):
        logging.debug('select_pcap_button_clicked(): Instantiated')
        pcap_file = QFileDialog()
        pcap_file.setWindowTitle("Select File")
        pcap_file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        pcap_file.setNameFilter("Zip Files (*.zip)")

        filenames = pcap_file.getOpenFileName()
        filename = filenames[0]
        if filename == "":
            logging.debug("File choose cancelled")
            return
        else:
            # Very similar to populate_import
            self.pcapNameLineEdit.setText(filename)
            if self.configname.text() != "":
                self.okButton.setEnabled(True)

    def on_ok_button_clicked(self):
        logging.debug('on_ok_button_clicked(): Instantiated')
        #Remove any special characters or spaces:
        self.projectName = self.configname.text()
        self.projectName = re.sub('\W+', '', self.projectName)
        
        #check if name has been filed out in order to create a project folder
        #with the name that was chosen:
        if self.projectName != '':
            self.projectPath = os.path.join(self.project_data_folder, self.projectName)
            #show the project name edited
            self.configname.setText(self.projectName)
            
            if os.path.exists(self.projectPath) == True:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "The project name specified and directory already exists",
                                        QMessageBox.Ok)            
                return None

        else:
            QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Project Name is Empty!",
                                        QMessageBox.Ok)
            return None

        #copy over the pcap (with a progress bar)
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.copy_completed)

        src_abs_filename = self.pcapNameLineEdit.text()
        src_filename = os.path.basename(src_abs_filename)
        dst_filename = os.path.join(self.projectPath, ConfigurationManager.STRUCTURE_PCAP_SUBDIR, str(src_filename))
        self.batch_thread.add_function(self.copy_PCAP, src_abs_filename, os.path.abspath(dst_filename))

        #create subdirectories (empty) for this project       
        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()
        
        logging.debug('on_ok_button_clicked(): Complete')

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def copy_completed(self):
        logging.debug('copy_completed(): Instantiated')
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        config = self.configname.text()
        self.existingconfignames[config] = self.pcapNameLineEdit.text()
        QMessageBox.about(self, "Completed", "Finished Setting Up Project")
        self.created.emit(config, self.existingconfignames, self.projectPath)
        self.close()
        logging.debug('copy_completed(): Completed')

    
    def on_cancel_button_clicked(self, event):
        logging.debug('on_cancel_button_clicked(): Instantiated')
        self.quit_event = event
        self.closeEvent(event)
        logging.debug('on_cancel_button_clicked(): Complete')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        self.close()
        return

    def copy_PCAP(self, src_filename, dst_filename):
        logging.debug('copy_PCAP(): Instantiated')
        try:
            dst_folder = os.path.dirname(dst_filename)
            if os.path.exists(dst_folder) == False:
                os.makedirs(dst_folder)
            shutil.copy2(src_filename, dst_folder)
        except:
            logging.error("generate_dissectors(): An error occured when trying to copy log files")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
