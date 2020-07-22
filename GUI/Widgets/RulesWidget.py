from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt

import os

class RulesWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBoxAnnot")

        self.setWindowTitle("ResultsWidget")
        self.setObjectName("ResultsWidget")

        #Label - Annotation Title
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
        pcapFolder = "PCAP/AnnotatedPCAP.pcapng"
        projectpcap = os.path.join(projectpath, pcapFolder)
        projectPCAPFolder = os.path.join(projectpath, "PCAP/")
        sessionPCAPFolder = os.path.join(projectPCAPFolder, sessionLabel)
        sessionPCAP = os.path.join(sessionPCAPFolder, "NeedsAnnotation.pcapng")

        #Change dir to session pcap folder
        os.chdir(sessionPCAPFolder)
        sessionRulesDirName = sessionLabel + "Rules"
        os.mkdir(sessionRulesDirName)

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
        self.pcapLineEdit2.setText(sessionPCAP)
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox2.addWidget(self.pcapLineEdit2)

         #Start Annotation Button
        self.ruleButtonHorBox = QtWidgets.QHBoxLayout()
        self.ruleButtonHorBox.setObjectName("ruleButtonHorBox")
        self.rulesButton = QPushButton("Generate Rules")
        #self.rulesButton.clicked.connect(lambda x: self.on_rules_button_clicked(x, sessionPCAP))
        self.ruleButtonHorBox.setAlignment(Qt.AlignRight)
        self.ruleButtonHorBox.addWidget(self.rulesButton)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.pcapHorBox)
        self.outerVertBox.addLayout(self.pcapHorBox2)
        self.outerVertBox.addLayout(self.ruleButtonHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

