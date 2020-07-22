from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QInputDialog, QMessageBox, QTextEdit
from PyQt5.QtCore import Qt
import logging

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner

class ProjectWidget(QtWidgets.QWidget):

    def __init__(self, projectname, projectpcap, projectpath):
        QtWidgets.QWidget.__init__(self, parent=None)
        #self.statusBar = statusBar
        self.projectItemNames = {}
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")

        self.setWindowTitle("ProjectWidget")
        self.setObjectName("ProjectWidget")

        #material widget - res
        #Project Name
        self.nameHorBox = QtWidgets.QHBoxLayout()
        self.nameHorBox.setObjectName("nameHorBox")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Project Name:")
        self.nameHorBox.addWidget(self.nameLabel)

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setAcceptDrops(False)
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setObjectName("nameLineEdit") 
        self.nameLineEdit.setText(projectname)     
        self.nameHorBox.addWidget(self.nameLineEdit)

        #Project Path
        self.pathHorBox = QtWidgets.QHBoxLayout()
        self.pathHorBox.setObjectName("pathHorBox")
        self.pathLabel = QtWidgets.QLabel()
        self.pathLabel.setObjectName("pathLabel")
        self.pathLabel.setText("Project Path:  ")
        self.pathHorBox.addWidget(self.pathLabel)

        self.pathLineEdit = QtWidgets.QLineEdit()
        self.pathLineEdit.setAcceptDrops(False)
        self.pathLineEdit.setReadOnly(True)
        self.pathLineEdit.setObjectName("pathLineEdit") 
        self.pathLineEdit.setText(projectpath)     
        self.pathHorBox.addWidget(self.pathLineEdit)

        self.projectPathViewButton = QPushButton("View")
        self.projectPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, projectpath))
        self.pathHorBox.addWidget(self.projectPathViewButton)

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

        #put all the components together
        self.outerVertBox.addLayout(self.nameHorBox)
        self.outerVertBox.addLayout(self.pathHorBox)
        self.outerVertBox.addLayout(self.pcapHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

    def addProjectItem(self, configname):
        logging.debug("addProjectItem(): retranslateUi(): instantiated")
        if configname in self.projectItemNames:
            logging.error("addprojectItem(): Item already exists in tree: " + str(configname))
            return

        logging.debug("addprojectItem(): retranslateUi(): Completed")
