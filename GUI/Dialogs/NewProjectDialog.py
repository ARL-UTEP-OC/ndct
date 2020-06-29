from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QTextEdit, QMessageBox, QSizePolicy, QAction, qApp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import logging
import os
import shutil

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Threading.BatchThread import BatchThread

class NewProjectDialog(QtWidgets.QWidget):
    #Signal for when the user is done creating the new project
    created = QtCore.pyqtSignal(str, list, str, str)
    logEnabled = QtCore.pyqtSignal(str)

    def __init__(self, logman, existingProjects):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.logger_started_once = False

        self.existingconfignames = existingProjects
        self.annotatedPCAP = ''
        self.projectPath = ""

        quit = QAction("Close", self)
        quit.triggered.connect(self.closeEvent)

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
        self.configname = QTextEdit()
        ###### Fixed Height for project name text box
        self.configname.setFixedHeight(27)

        #Create buttons for creating new file
        self.logOutStartButton = QPushButton("Start Logging")
        self.logOutStopButton = QPushButton("Stop Logging")
        self.logOutSaveButton = QPushButton("Save/Create")
        self.logOutCancelButton = QPushButton("Cancel")

        #Add on click event
        self.logOutStartButton.clicked.connect(self.on_log_start_button_clicked)
        self.logOutStartButton.setEnabled(True)
        self.logOutStopButton.clicked.connect(self.on_log_stop_button_clicked)
        self.logOutStopButton.setEnabled(True)
        self.logOutSaveButton.clicked.connect(self.on_log_save_button_clicked)
        self.logOutSaveButton.setEnabled(True)
        self.logOutCancelButton.clicked.connect(self.on_cancel_button_clicked)

        #Set the button layouts
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #Put all the components together
        self.nameVerBoxPro.addWidget(self.configname)
        self.bottomButtons_layout.addWidget(self.logOutStartButton)
        self.bottomButtons_layout.addWidget(self.logOutStopButton)
        self.bottomButtons_layout.addWidget(self.logOutSaveButton)
        self.bottomButtons_layout.addWidget(self.logOutCancelButton, alignment=QtCore.Qt.AlignRight)
        
        self.outerVertBoxPro.addLayout(self.nameVerBoxPro)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.setLayout(self.outerVertBoxPro)

        self.logman = logman
    
    def on_log_start_button_clicked(self):
        logging.debug('on_log_start_button_clicked(): Instantiated')
        #check if name has been filed out in order to create a project folder
        #with the name that was chosen:
        if self.configname.toPlainText() != '':
            self.projectPath = os.path.join("/home/kali/eceld-netsys/ProjectData", self.configname.toPlainText())
            
            if self.logger_started_once == True and os.path.exists(self.projectPath) == True:
                buttonReply = QMessageBox.question(self, 'Confirmation', "Restarting the Logger will Remove any Previous Data. \r\n Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                shutil.rmtree(self.projectPath)
                if buttonReply != QMessageBox.Yes:
                    logging.debug('on_log_start_button_clicked(): Cancelled')
                    return
            if os.path.exists(self.projectPath) == True:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "The project name specified and directory already exists",
                                        QMessageBox.Ok)            
                return None
            
            
            self.logger_started_once = True
            self.logman.remove_data_all()
            self.logman.start_collectors()

            self.logEnabled.emit("TRUE")

            self.logOutStartButton.setEnabled(False)
            self.logOutStopButton.setEnabled(True)
        else:
            QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Project Name is Empty!",
                                        QMessageBox.Ok) 

        logging.debug('on_log_start_button_clicked(): Complete')

    def on_log_stop_button_clicked(self):
        logging.debug('on_log_stop_button_clicked(): Instantiated')

        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.stop_button_batch_completed)
        
        self.batch_thread.add_function(self.logman.stop_collectors)
        self.batch_thread.add_function(self.logman.parse_data_all)
        self.batch_thread.add_function(self.logman.export_data, self.projectPath)
        parsedLogs = os.path.join(self.projectPath,ConfigurationManager.STRUCTURE_PARSED_PATH)
        annotatedPCAP = os.path.join(self.projectPath, ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
        self.batch_thread.add_function(self.logman.copy_latest_data, self.projectPath, parsedLogs, annotatedPCAP)
        dissectorsPath = os.path.join(self.projectPath, ConfigurationManager.STRUCTURE_GEN_DISSECTORS_PATH)
        self.batch_thread.add_function(self.logman.generate_dissectors, parsedLogs, dissectorsPath, None)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        self.logOutSaveButton.setEnabled(True)
        
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
            QMessageBox.about(self, "Processing Complete", "No files processed")
        else: 
            QMessageBox.about(self, "Processing Complete", output_dissected)
            
            self.logOutStartButton.setEnabled(True)
            self.logOutStopButton.setEnabled(False)
            self.annotatedPCAP = os.path.join(self.projectPath, ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
            self.logEnabled.emit("FALSE")
            
        logging.debug('thread_finish(): Completed')

    def on_log_save_button_clicked(self):
        logging.debug('on_log_save_button_clicked(): Instantiated')

        if self.configname.toPlainText() != '':
            if self.configname.toPlainText() in self.existingconfignames and os.path.exists(self.projectPath) == True:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "The project name specified and directory already exists",
                                        QMessageBox.Ok)            
                return None
            else:
                #if all good, add to existing file names list
                self.existingconfignames += [self.configname.toPlainText()]

                saveComplete = QMessageBox.warning(self,
                                                    "Creation Successful",
                                                    "Success! Project Created.",
                                                    QMessageBox.Ok)
                #Once save is hit, it should close the new project pop up and return to the main window
                if saveComplete == QMessageBox.Ok:
                    #let main window know everything is ready:
                    #Send signal to slot
                    config = self.configname.toPlainText()
                    self.created.emit(config, self.existingconfignames, self.annotatedPCAP, self.projectPath)
                    self.close()
        else:
             QMessageBox.warning(self,
                                        "Name is Empty",
                                        "Project Name is Empty!",
                                        QMessageBox.Ok)  

        logging.debug('on_log_save_button_clicked(): Complete')
    
    def on_cancel_button_clicked(self, event):
        logging.debug('on_cancel_button_clicked(): Instantiated')

        cancel = QMessageBox.question(
            self, "Close New Project",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Close | QMessageBox.Cancel)

        if cancel == QMessageBox.Close:
            self.close()
        else:
            pass

        logging.debug('on_cancel_button_clicked(): Complete')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")
        self.quit_event = event
        if self.logOutStartButton.isEnabled() == True:
            event.accept()
            self.close()
        if self.logOutStartButton.isEnabled() == False:
            close = QMessageBox.question(self,
                                            "CLOSE",
                                            "Logger is running. Stop and Close?",
                                            QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                logging.debug("closeEvent(): Creating Quit Command Load")
                self.batch_thread = BatchThread()
                self.batch_thread.progress_signal.connect(self.update_progress_bar)
                #self.batch_thread.completion_signal.connect(self.close)
                
                self.batch_thread.add_function(self.logman.stop_collectors)
                self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
                self.batch_thread.start()
                self.progress_dialog_overall.show()
                self.batch_thread.completion_signal.connect(self.quit_app)
                return
        else:
            pass
        logging.debug("closeEvent(): returning ignore")
        return

    def quit_app(self):
        self.destroy()
        self.quit_event.accept()
        self.progress_dialog_overall.hide()
        return
