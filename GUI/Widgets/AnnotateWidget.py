from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import os
from shutil import copy2

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner

class AnnotateWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBoxAnnot")

        self.setWindowTitle("AnnotateWidget")
        self.setObjectName("AnnotateWidget")

        #Label - Annotation Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.annLabel = QtWidgets.QLabel("ANNOTATE")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.annLabel.setFont(labelFont)
        self.annLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxSess.addWidget(self.annLabel)

        #Project PCAP
        self.pcapHorBox = QtWidgets.QHBoxLayout()
        self.pcapHorBox.setObjectName("pcapHorBox")
        self.pcapLabel = QtWidgets.QLabel()
        self.pcapLabel.setObjectName("pcapLabel")
        self.pcapLabel.setText("Project PCAP:  ")
        self.pcapHorBox.addWidget(self.pcapLabel)

        #get project pcap path
        projectpath = os.path.join(projectfolder, projectName)
        pcapFolder = "PCAP/AnnotatedPCAP.pcapng"
        projectpcap = os.path.join(projectpath, pcapFolder)
        projectPCAPFolder = os.path.join(projectpath, "PCAP/")

        #make a copy of the pcap and save it to a new folder based on session
        os.chdir(projectPCAPFolder)
        os.mkdir(sessionLabel)
        sessionFolder = os.path.join(projectPCAPFolder,sessionLabel)
        copy2(projectpcap, sessionFolder)
        sessionPCAP = os.path.join(sessionFolder, "AnnotatedPCAP.pcapng")
        os.chdir(sessionFolder)
        os.rename(sessionPCAP, "NeedsAnnotation.pcapng")
        sessionPCAP = os.path.join(sessionFolder, "NeedsAnnotation.pcapng")

        self.pcapLineEdit = QtWidgets.QLineEdit()
        self.pcapLineEdit.setAcceptDrops(False)
        self.pcapLineEdit.setReadOnly(True)
        self.pcapLineEdit.setObjectName("pcapLineEdit") 
        self.pcapLineEdit.setText(projectpcap)
        self.pcapLineEdit.setAlignment(Qt.AlignLeft)    
        self.pcapHorBox.addWidget(self.pcapLineEdit)

        #show corresponding folder for annoatation pcap
        self.sessPCAPHorBox = QtWidgets.QHBoxLayout()
        self.sessPCAPHorBox.setObjectName("sessPCAPHorBox")
        self.sessPCAPLabel = QtWidgets.QLabel()
        self.sessPCAPLabel.setObjectName("sessPCAPLabel")
        self.sessPCAPLabel.setText("PCAP to be Annotated: ")
        self.sessPCAPHorBox.addWidget(self.sessPCAPLabel)

        self.pcapLineEdit2 = QtWidgets.QLineEdit()
        self.pcapLineEdit2.setAcceptDrops(False)
        self.pcapLineEdit2.setReadOnly(True)
        self.pcapLineEdit2.setObjectName("pcapLineEdit2") 
        self.pcapLineEdit2.setText(sessionPCAP)
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)
        self.sessPCAPHorBox.addWidget(self.pcapLineEdit2)

        #Start Annotation Button
        self.annButtonHorBox = QtWidgets.QHBoxLayout()
        self.annButtonHorBox.setObjectName("annButtonHorBox")
        self.annotationButton = QPushButton("Annotate PCAP")
        self.annotationButton.clicked.connect(lambda x: self.on_annotate_button_clicked(x, sessionPCAP))
        self.annButtonHorBox.setAlignment(Qt.AlignRight)
        self.annButtonHorBox.addWidget(self.annotationButton)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.pcapHorBox)
        self.outerVertBox.addLayout(self.sessPCAPHorBox)
        self.outerVertBox.addLayout(self.annButtonHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def on_annotate_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()

        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

