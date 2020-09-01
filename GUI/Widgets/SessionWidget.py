from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt

class SessionWidget(QtWidgets.QWidget):

    def __init__(self, sessionName):
        QtWidgets.QWidget.__init__(self, parent=None)
        
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")

        self.setWindowTitle("SessionWidget")
        self.setObjectName("SessionWidget")

        #Label - Session Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.sessLabel = QtWidgets.QLabel("SESSION")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.sessLabel.setFont(labelFont)
        self.sessLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxSess.addWidget(self.sessLabel)

        #Display Session Name
        self.nameHorBox = QtWidgets.QHBoxLayout()
        self.nameHorBox.setObjectName("nameHorBox")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Session Name:")
        self.nameHorBox.addWidget(self.nameLabel)

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setAcceptDrops(False)
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setObjectName("nameLineEdit") 
        self.nameLineEdit.setText(sessionName)     
        self.nameHorBox.addWidget(self.nameLineEdit)

        #put all the components together
        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.outerVertBox.addLayout(self.nameHorBox)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)
