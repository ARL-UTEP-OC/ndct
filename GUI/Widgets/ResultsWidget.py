from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import os

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner

class ResultsWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel, resultsDir):
        QtWidgets.QWidget.__init__(self, parent=None)

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
        sessionPCAP = os.path.join(sessionPCAPFolder, "NeedsAnnotation.pcapng")
        sessionRulesDirName = sessionLabel + "Rules"
        sessionRulesDirName = os.path.join(sessionPCAPFolder, sessionRulesDirName)

        #Path to where the rules stored
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
        self.ruleLineEdit.setText(sessionRulesDirName)
        self.ruleLineEdit.setAlignment(Qt.AlignLeft)
        self.ruleHorBox.addWidget(self.ruleLineEdit)

        #Annotated/Suspect PCAP
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
        self.pcapLineEdit2.setText(sessionPCAP)
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox2.addWidget(self.pcapLineEdit2)

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
        self.alertLineEdit.setText(resultsDir)
        self.alertLineEdit.setAlignment(Qt.AlignLeft)
        self.alertHorBox.addWidget(self.alertLineEdit)

        self.alertPathViewButton = QPushButton("View")
        self.alertPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, resultsDir))
        self.alertHorBox.addWidget(self.alertPathViewButton)

        #Generate Alerts Button
        self.alertButtonHorBox = QtWidgets.QHBoxLayout()
        self.alertButtonHorBox.setObjectName("alertButtonHorBox")
        self.alertButton = QPushButton("Generate Alerts")
        #self.alertButton.clicked.connect(lambda x: self.on_alert_button_clicked(x, sessionPCAP))
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
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()
