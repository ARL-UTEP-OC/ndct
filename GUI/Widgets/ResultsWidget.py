from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class ResultsWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")

        self.setWindowTitle("RulesWidget")
        self.setObjectName("RulesWidget")

        #Label - Session Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.sessionLabel = QLabel("Results")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.sessionLabel.setFont(labelFont)
        self.sessionLabel.setAlignment(Qt.AlignCenter)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.setFixedSize(self.labelVerBoxSess.sizeHint())

        self.setLayout(self.outerVertBox)