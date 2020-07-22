from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class AnnotateWidget(QtWidgets.QWidget):

    def __init__(self):
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

        self.outerVertBox.addLayout(self.labelVerBoxSess)

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)