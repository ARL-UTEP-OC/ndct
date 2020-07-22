from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class RulesWidget(QtWidgets.QWidget):

    def __init__(self):
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

        self.outerVertBox.addLayout(self.labelVerBoxSess)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)