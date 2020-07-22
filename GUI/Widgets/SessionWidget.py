from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
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

        self.sessionLabel = QLabel(sessionName)
        print("IN SESSION, NAME IS: " + sessionName)
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.sessionLabel.setFont(labelFont)
        self.sessionLabel.setAlignment(Qt.AlignCenter)
        
        #put components together
        self.labelVerBoxSess.addWidget(self.sessionLabel)
        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.setFixedSize(self.labelVerBoxSess.sizeHint())

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)
