from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class ResultsWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBoxAnnot")

        self.setWindowTitle("ResultsWidget")
        self.setObjectName("ResultsWidget")

        #Label - Annotation Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.resultLabel = QtWidgets.QLabel("RESULTS")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.resultLabel.setFont(labelFont)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxSess.addWidget(self.resultLabel)

        self.outerVertBox.addLayout(self.labelVerBoxSess)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)