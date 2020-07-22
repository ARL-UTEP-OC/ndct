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

        #Label - Session Title
        self.labelVerBoxSess = QtWidgets.QVBoxLayout()
        self.labelVerBoxSess.setObjectName("labeVerBoxPro")
        self.sessionLabel = QLabel("ANNOTATE")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.sessionLabel.setFont(labelFont)
        self.sessionLabel.setAlignment(Qt.AlignCenter)

        self.outerVertBox.addLayout(self.labelVerBoxSess)
        self.setFixedSize(self.labelVerBoxSess.sizeHint())

        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)