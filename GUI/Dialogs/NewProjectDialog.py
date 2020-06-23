from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QPlainTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import logging

class NewProjectDialog(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("New Project")
        self.setObjectName("NewProjectDialog")

        self.nameVerBoxPro = QtWidgets.QHBoxLayout()
        self.nameVerBoxPro.setObjectName("nameVerBoxPro")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Type in New Project Name:")
        self.nameVerBoxPro.addWidget(self.nameLabel)
        self.configname = QtWidgets.QLineEdit()

        #Create buttons for creating new file
        self.pathLabel = QtWidgets.QLabel()
        self.pathLabel.setObjectName("pathLabel")
        self.pathLabel.setText("Select Directory to Save Project:")
        self.logOutPathEdit = QtWidgets.QLineEdit()
        self.logOutPathEdit.setObjectName("logOutPathEdit")
        self.logOutPathEdit.setAlignment(Qt.AlignLeft)
        self.logOutPathButton = QPushButton("...")
        self.logOutViewButton = QPushButton("View")
        self.logOutStartButton = QPushButton("Start Logging")
        self.logOutStopButton = QPushButton("Stop")
        self.logOutSaveButton = QPushButton("Save")
        #cancel
        self.logOutCancelButton = QPushButton("Cancel")

        #Set the button layouts
        self.pathLabel_layout = QtWidgets.QVBoxLayout()
        self.pathEdit_layout = QtWidgets.QHBoxLayout()
        self.bottomButtons_layout = QtWidgets.QHBoxLayout()

        #Put all the components together
        self.nameVerBoxPro.addWidget(self.configname)
        self.pathLabel_layout.addWidget(self.pathLabel)
        self.pathEdit_layout.addWidget(self.logOutPathEdit)
        self.pathEdit_layout.addWidget(self.logOutPathButton)
        self.pathEdit_layout.addWidget(self.logOutViewButton)
        self.bottomButtons_layout.addWidget(self.logOutStartButton)
        self.bottomButtons_layout.addWidget(self.logOutStopButton)
        self.bottomButtons_layout.addWidget(self.logOutSaveButton)
        self.bottomButtons_layout.addWidget(self.logOutCancelButton, alignment=QtCore.Qt.AlignRight)
        
        self.outerVertBoxPro.addLayout(self.nameVerBoxPro)
        self.outerVertBoxPro.addLayout(self.pathLabel_layout)
        self.outerVertBoxPro.addLayout(self.pathEdit_layout)
        self.outerVertBoxPro.addLayout(self.bottomButtons_layout)

        self.outerVertBoxPro.addStretch()

        self.paddingWidget1 = QtWidgets.QWidget()
        self.paddingWidget1.setObjectName("paddingWidget1")
        self.outerVertBoxPro.addWidget(self.paddingWidget1)
        self.paddingWidget2 = QtWidgets.QWidget()
        self.paddingWidget2.setObjectName("paddingWidget2")
        self.outerVertBoxPro.addWidget(self.paddingWidget2)
        self.paddingWidget3 = QtWidgets.QWidget()
        self.paddingWidget3.setObjectName("paddingWidget3")
        self.outerVertBoxPro.addWidget(self.paddingWidget3)

        self.setLayout(self.outerVertBoxPro)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = NewProjectDialog()
    ui.show()
    sys.exit(app.exec_())