from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt

import os
import logging

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from GUI.Threading.BatchThread import BatchThread
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

class RulesWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel, rulesDir, comment_mgr, val):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.rulesDir = rulesDir
        self.comment_mgr = comment_mgr
        self.val = val

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBoxAnnot")

        self.setWindowTitle("RulesWidget")
        self.setObjectName("RulesWidget")

        #Label - Rules Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.rulesLabel = QtWidgets.QLabel("RULES")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.rulesLabel.setFont(labelFont)
        self.rulesLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxSess.addWidget(self.rulesLabel)

        #get project pcap path

        projectpath = os.path.join(projectfolder, projectName)
        projectPCAPFolder = os.path.join(projectpath, "PCAP/")
        projectpcap = os.path.join(projectPCAPFolder, "AnnotatedPCAP.pcapng")

        sessionPCAPFolder = os.path.join(projectPCAPFolder, sessionLabel)
        self.sessionPCAP = os.path.join(sessionPCAPFolder, "NeedsAnnotation.pcapng")

        #create a directory for session rules
        self.sessionRulesDir = os.path.join(rulesDir, sessionLabel)

        #if corresponding session dir doesnt exist, create dir
        if os.path.exists(self.sessionRulesDir) == False:
            os.mkdir(self.sessionRulesDir)
        
        #Project PCAP
        self.pcapHorBox = QtWidgets.QHBoxLayout()
        self.pcapHorBox.setObjectName("pcapHorBox")
        self.pcapLabel = QtWidgets.QLabel()
        self.pcapLabel.setObjectName("pcapLabel")
        self.pcapLabel.setText("Project PCAP:  ")
        self.pcapHorBox.addWidget(self.pcapLabel)

        self.pcapLineEdit = QtWidgets.QLineEdit()
        self.pcapLineEdit.setAcceptDrops(False)
        self.pcapLineEdit.setReadOnly(True)
        self.pcapLineEdit.setObjectName("pcapLineEdit") 
        self.pcapLineEdit.setText(projectpcap)
        self.pcapLineEdit.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox.addWidget(self.pcapLineEdit)

        self.pcapPathViewButton = QPushButton("View")
        self.pcapPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, projectPCAPFolder))
        self.pcapHorBox.addWidget(self.pcapPathViewButton)

        #Annotated PCAP
        self.pcapHorBox2 = QtWidgets.QHBoxLayout()
        self.pcapHorBox2.setObjectName("pcapHorBox2")
        self.pcapLabel2 = QtWidgets.QLabel()
        self.pcapLabel2.setObjectName("pcapLabel2")
        self.pcapLabel2.setText("Annotated PCAP:  ")
        self.pcapHorBox2.addWidget(self.pcapLabel2)

        self.pcapLineEdit2 = QtWidgets.QLineEdit()
        self.pcapLineEdit2.setAcceptDrops(False)
        self.pcapLineEdit2.setReadOnly(True)
        self.pcapLineEdit2.setObjectName("pcapLineEdit2") 
        self.pcapLineEdit2.setText(self.sessionPCAP)
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox2.addWidget(self.pcapLineEdit2)

        self.pcapPathViewButton2 = QPushButton("View")
        self.pcapPathViewButton2.clicked.connect(lambda x: self.on_view_button_clicked(x, sessionPCAPFolder))
        self.pcapHorBox2.addWidget(self.pcapPathViewButton2)

        #Generate Rules Button
        self.ruleButtonHorBox = QtWidgets.QHBoxLayout()
        self.ruleButtonHorBox.setObjectName("ruleButtonHorBox")
        self.rulesButton = QPushButton("Generate Rules")
        self.rulesButton.clicked.connect(self.on_rules_button_clicked)
        self.ruleButtonHorBox.setAlignment(Qt.AlignRight)
        self.ruleButtonHorBox.addWidget(self.rulesButton)

        #Path to where the rules are going to be outputted
        self.ruleHorBox = QtWidgets.QHBoxLayout()
        self.ruleHorBox.setObjectName("ruleHorBox")
        self.rulePathLabel = QtWidgets.QLabel()
        self.rulePathLabel.setObjectName("rulePathLabel")
        self.rulePathLabel.setText("Rule Output Path: ")
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

        #put everything together
        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.pcapHorBox)
        self.outerVertBox.addLayout(self.pcapHorBox2)
        self.outerVertBox.addLayout(self.ruleHorBox)
        self.outerVertBox.addLayout(self.ruleButtonHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

    def on_rules_button_clicked(self):
        logging.debug('on_genrules_out_start_button_clicked(): Instantiated')
        
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.genrules_button_batch_completed)

        self.batch_thread.add_function( self.comment_mgr.extract_json, self.sessionPCAP)
        comment_filename = os.path.join(self.sessionRulesDir, ConfigurationManager.STRUCTURE_JSON_COMMENTS)
        self.batch_thread.add_function( self.comment_mgr.write_comment_json_to_file, comment_filename)

        self.batch_thread.add_function( self.val.extract_rules, comment_filename)
        rules_filename = os.path.join(self.sessionRulesDir, ConfigurationManager.STRUCTURE_RULES_GEN_FILE)
        self.batch_thread.add_function( self.val.write_rules_to_file, rules_filename)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

        logging.debug('on_genrules_out_start_button_clicked(): Complete')

    def genrules_button_batch_completed(self):
        logging.debug('thread_finish(): Instantiated')

        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()

        logging.debug('thread_finish(): Completed')

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')