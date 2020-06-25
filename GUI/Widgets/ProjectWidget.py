from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
import logging

class ProjectWidget(QtWidgets.QWidget):

    def __init__(self, projectname, projectpath, projectpcap):
        QtWidgets.QWidget.__init__(self, parent=None)
        #self.statusBar = statusBar
        self.projectItemNames = {}
        self.existingSessionNames = []
        self.sessionName = ''
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

        #Push button to begin annotating - to create a new session
        self.projectAddSession = QPushButton("New Session")
        self.projectAddSession.clicked.connect(self.on_new_session_button_clicked)
        self.projectAddSession.setEnabled(True)
        #session layout
        self.session_button_layout = QtWidgets.QHBoxLayout()
        self.session_button_layout.addWidget(self.projectAddSession)

        #put all the components together
        self.outerVertBox.addLayout(self.nameHorBox)
        self.outerVertBox.addLayout(self.pathHorBox)
        self.outerVertBox.addLayout(self.pcapHorBox)
        self.outerVertBox.addLayout(self.session_button_layout)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def addProjectItem(self, configname):
        logging.debug("addProjectItem(): retranslateUi(): instantiated")
        if configname in self.projectItemNames:
            logging.error("addprojectItem(): Item already exists in tree: " + str(configname))
            return

        logging.debug("addprojectItem(): retranslateUi(): Completed")
    
    def on_new_session_button_clicked(self):
        logging.debug("on_new_session_button_clicked(): Instantiated")

        ok = QInputDialog.getText(self, 'New Session', 
            'Enter new session name \r\n(non alphanumeric characters will be removed)')
        if ok:
            self.sessionName = ''.join(e for e in self.sessionName if e.isalnum())
            if self.sessionName in self.existingSessionNames:
                if self.configname in self.existingconfignames:
                    QMessageBox.warning(self.parent,
                                        "Session Name Exists",
                                        "The session name specified already exists",
                                        QMessageBox.Ok)            
                return None

        logging.debug("on_new_session_button_clicked(): Completed")
