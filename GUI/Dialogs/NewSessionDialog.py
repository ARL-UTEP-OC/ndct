from PyQt5.QtWidgets import QComboBox, QFileDialog, QListView, QWidget, QPushButton, QTextEdit, QMessageBox, QSizePolicy, QAction, qApp, QLabel, QLineEdit
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

class NewSessionDialog(QtWidgets.QWidget):
    #Signal for when the user is done creating the new session
    created = QtCore.pyqtSignal(str)
    def __init__(self, projectName):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.logger_started_once = False

        self.projectPath = ""
        self.projectName = projectName
        self.cancel_pressed = False
        self.saved_pressed = False
        self.cm = ConfigurationManager.get_instance()
        self.project_sessions_folder = self.cm.read_config_value("PROJECTS", "PROJECTS_BASE_PATH")
        self.project_sessions_folder = os.path.join(self.project_sessions_folder, self.projectName)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("Create Session")
        self.setObjectName("New Project Session")

        #Label - New Session Title
        self.labelVerBoxPro = QtWidgets.QVBoxLayout()
        self.labelVerBoxPro.setObjectName("labeVerBoxPro")
        self.newSessionLabel = QLabel("Create Session")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.newSessionLabel.setFont(labelFont)
        self.newSessionLabel.setAlignment(Qt.AlignCenter)

        self.sessionNameHorBoxPro = QtWidgets.QHBoxLayout()
        self.sessionNameHorBoxPro.setObjectName("sessionNameHorBoxPro")
        self.sessionNameLabel = QtWidgets.QLabel()
        self.sessionNameLabel.setObjectName("sessionNameLabel")
        self.sessionNameLabel.setText("Session Name:")
        self.sessionNameHorBoxPro.addWidget(self.sessionNameLabel)
        self.newsessionname = QLineEdit()
        self.newsessionname.textChanged.connect(self.on_newsessionname_changed)
        self.newsessionname.setFixedHeight(27)
        self.sessionNameHorBoxPro.addWidget(self.newsessionname)

        self.templateNameHorBoxPro = QtWidgets.QHBoxLayout()
        self.templateNameHorBoxPro.setObjectName("templateNameHorBoxPro")
        self.templateNameLabel = QtWidgets.QLabel()
        self.templateNameLabel.setObjectName("templateNameLabel")
        self.templateNameLabel.setText("From Session:")
        self.templateNameHorBoxPro.addWidget(self.templateNameLabel)
        self.templateNameComboBox = QComboBox()
        self.templateNameComboBox.addItem("None")
        self.templateNameComboBox.setEnabled(False)
        self.templateNameComboBox.setFixedHeight(27)
        self.templateNameHorBoxPro.addWidget(self.templateNameComboBox)

        #Create buttons for OK/Cancel
        self.okButton = QPushButton("OK")
        self.okButton.setEnabled(False)
        self.okButton.clicked.connect(self.on_ok_button_clicked)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.on_cancel_button_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #Put all the components together
        self.labelVerBoxPro.addWidget(self.newSessionLabel)
        self.bottomButtons_layout.addWidget(self.okButton)
        self.bottomButtons_layout.addWidget(self.cancelButton, alignment=QtCore.Qt.AlignRight)
        
        self.outerVertBoxPro.addLayout(self.labelVerBoxPro)
        self.outerVertBoxPro.addLayout(self.sessionNameHorBoxPro)
        self.outerVertBoxPro.addLayout(self.templateNameHorBoxPro)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.setLayout(self.outerVertBoxPro)
    
    def on_newsessionname_changed(self):
        #logging.debug('on_configname_changed(): Instantiated')
        if self.newsessionname.text() != "":
            self.okButton.setEnabled(True)
        else:
            self.okButton.setEnabled(False)

    def on_ok_button_clicked(self):
        logging.debug('on_ok_button_clicked(): Instantiated')
        #Remove any special characters or spaces:
        self.sessionName = self.newsessionname.text()
        self.sessionName = re.sub('\W+', '', self.sessionName)
        
        #check if name has been filed out in order to create a session folder
        #with the name that was chosen:
        if self.sessionName != '':
            self.sessionPath = os.path.join(self.project_sessions_folder, self.sessionName)
            #show the project name edited
            self.newsessionname.setText(self.sessionName)
            
            if os.path.exists(self.sessionPath) == True:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "The session name specified and directory already exists",
                                        QMessageBox.Ok)            
                return None

        else:
            QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Session Name is Empty!",
                                        QMessageBox.Ok)
            return None

        #copy over the pcap (with a progress bar)
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.create_session_completed)

        #TODO: check if template chosen and then add the function call
        if self.templateNameComboBox.currentText() == "None":
            self.batch_thread.add_function(self.create_session, self.newsessionname.text())
        else:
            self.batch_thread.add_function(self.create_session, self.newsessionname.text(), self.templateNameComboBox.currentText())

        #create subdirectories (empty) for this project       
        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()
        
        logging.debug('on_ok_button_clicked(): Complete')

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def create_session_completed(self):
        logging.debug('copy_completed(): Instantiated')
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        newsessionname = self.newsessionname.text()
        QMessageBox.about(self, "Completed", "Finished Setting Up Session")
        
        self.created.emit(newsessionname)
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
        self.progress_dialog_overall.close()
        self.close()
        return

    def create_session(self, session_name, template_name=None):
        logging.debug("create_session(): instantiated")
        try:
            if template_name != None:
                #first copy required
                logging.debug("Creating session " + str(session_name) + " from template: " + str(template_name))
                if template_name.startswith("S: "):
                    logging.debug("Removing Preceeding characters from template name: " + str(template_name))
                    template_name = template_name.split("S: ",1)[1]
                    logging.debug("New template name: " + str(template_name))
                templatePathPCAP = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_PCAP_SUBDIR, template_name)
                dstSessionPCAP = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_PCAP_SUBDIR, session_name)
                if os.path.exists(templatePathPCAP):
                    logging.debug("Template PCAP Path exists: " + str(templatePathPCAP))
                    if os.path.exists(dstSessionPCAP):
                        logging.debug("Session PCAP Path already exists, removing: " + str(dstSessionPCAP))
                        shutil.rmtree(dstSessionPCAP)
                    logging.debug("Copying Template PCAP " + str(templatePathPCAP) + " to New Session: " + str(dstSessionPCAP))
                    res_dir = shutil.copytree(templatePathPCAP, dstSessionPCAP)
                else:
                    logging.error("PCAP for Template Session does not exist: " + str(template_name))
                    return

                templatePathRULES = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_RULES_GEN_PATH, template_name)
                dstSessionPathRULES = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_RULES_GEN_PATH, session_name)
                if os.path.exists(templatePathRULES):
                    if os.path.exists(dstSessionPathRULES):
                        shutil.rmtree(dstSessionPathRULES)
                    res_dir = shutil.copytree(templatePathRULES, dstSessionPathRULES)
                else:
                    logging.debug("RULES PATH for Template Session does not exist: " + str(template_name))

                templatePathIDS_ALERTS = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_ALERT_GEN_PATH, template_name)
                dstPathIDS_ALERTS = os.path.join(self.project_sessions_folder, ConfigurationManager.STRUCTURE_ALERT_GEN_PATH, session_name)
                if os.path.exists(templatePathIDS_ALERTS):
                    if os.path.exists(dstPathIDS_ALERTS):
                        shutil.rmtree(dstPathIDS_ALERTS)
                    res_dir = shutil.copytree(templatePathIDS_ALERTS, dstPathIDS_ALERTS)
                else:
                    logging.debug("RULES PATH for Template Session does not exist: " + str(template_name))
                
        except:
            logging.error("create_session(): An error occured when trying to copy session folders")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)                

    def copy_Session(self, src_folder, dst_folder):
        logging.debug('copy_Session(): Instantiated')
        try:
            dst_folder = os.path.dirname(dst_folder)
            if os.path.exists(dst_folder) == False:
                os.makedirs(dst_folder)
            shutil.copy2(src_folder, dst_folder)
        except:
            logging.error("copy_Session(): An error occured when trying to copy log files")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
