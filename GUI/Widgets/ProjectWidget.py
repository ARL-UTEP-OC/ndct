#from ExperimentActionsWidget - RES
from PyQt5 import QtCore, QtGui, QtWidgets
import logging

class ProjectWidget(QtWidgets.QWidget):

    def __init__(self, projectname, projectpath):
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
        self.pathLineEdit.setObjectName("nameLineEdit") 
        self.pathLineEdit.setText(projectpath)     
        self.pathHorBox.addWidget(self.pathLineEdit)

        self.outerVertBox.addLayout(self.nameHorBox)
        self.outerVertBox.addLayout(self.pathHorBox)
        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

    def addProjectItem(self, configname):
        logging.debug("addProjectItem(): retranslateUi(): instantiated")
        if configname in self.projectItemNames:
            logging.error("addprojectItem(): Item already exists in tree: " + str(configname))
            return

        logging.debug("addprojectItem(): retranslateUi(): Completed")
