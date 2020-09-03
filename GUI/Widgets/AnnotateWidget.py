from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import os
import sys, traceback
from shutil import copy2
import logging

from ConfigurationManager.FileExplorerRunner import ConfigurationManager
from GUI.Threading.BatchThread import BatchThread
from ConfigurationManager.FileExplorerRunner import FileExplorerRunner


class AnnotateWidget(QtWidgets.QWidget):

    def __init__(self, projectfolder, projectName, sessionLabel, comment_mgr):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.comment_mgr = comment_mgr

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

        os.chdir(projectPCAPFolder)
        sessionFolder = os.path.join(projectPCAPFolder,sessionLabel)

        if os.path.exists(sessionFolder) == False:
            os.mkdir(sessionLabel)
        #check if already exists (in case of import or reopen application)
        sessionPCAP_Annotated = os.path.join(sessionFolder, "NeedsAnnotation.pcapng")
        if os.path.exists(sessionPCAP_Annotated) == False:
            try:
                copy2(projectpcap, sessionPCAP_Annotated)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.error("AnnotateWidget init(): An error occured ")
                traceback.print_exception(exc_type, exc_value, exc_traceback)


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
        self.pcapLineEdit2.setText(sessionPCAP_Annotated)
        self.pcapLineEdit2.setAlignment(Qt.AlignLeft)
        self.sessPCAPHorBox.addWidget(self.pcapLineEdit2)

        self.sesspcapPathViewButton = QPushButton("View")
        self.sesspcapPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, sessionFolder))
        self.sessPCAPHorBox.addWidget(self.sesspcapPathViewButton)

        #Start Annotation Button
        self.annButtonHorBox = QtWidgets.QHBoxLayout()
        self.annButtonHorBox.setObjectName("annButtonHorBox")
        self.annotationButton = QPushButton("Annotate PCAP")
        self.annotationButton.clicked.connect(lambda x: self.on_annotate_button_clicked(x, sessionPCAP_Annotated, projectpath))
        self.annButtonHorBox.setAlignment(Qt.AlignRight)
        self.annButtonHorBox.addWidget(self.annotationButton)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.pcapHorBox)
        self.outerVertBox.addLayout(self.sessPCAPHorBox)
        self.outerVertBox.addLayout(self.annButtonHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def on_annotate_button_clicked(self, x, session_pcap=None, project_path=None):
        logging.debug('on_select_annotate_file_button_clicked(): Instantiated')
        #open wireshark using pcap and provide base so that the dissectors can be found
        user_pcap_filename = session_pcap
        #pcapBasepath = os.path.dirname(os.path.dirname(session_pcap))
        dissectors_path = os.path.join(project_path, ConfigurationManager.STRUCTURE_GEN_DISSECTORS_PATH)
        logging.debug("Checking if path exists: " + str(dissectors_path))
        if os.path.exists(dissectors_path):
            self.comment_mgr.run_wireshark_with_dissectors(project_path, user_pcap_filename)
        else:
            self.comment_mgr.run_wireshark_with_dissectors([], session_pcap)
        
        logging.debug('on_select_annotate_file_button_clicked(): Complete')

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()