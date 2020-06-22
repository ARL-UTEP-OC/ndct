#from ExperimentActionsWidget - RES
from PyQt5 import QtCore, QtGui, QtWidgets
import logging

class ProjectWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        #self.statusBar = statusBar
        self.projectItemNames = {}
        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")

        self.setWindowTitle("ProjectWidget")
        self.setObjectName("ProjectWidget")

        #material widget - res
        self.nameHorBox = QtWidgets.QHBoxLayout()
        self.nameHorBox.setObjectName("nameHorBox")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Name:")
        self.nameHorBox.addWidget(self.nameLabel)

        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setAcceptDrops(False)
        self.nameLineEdit.setReadOnly(True)
        self.nameLineEdit.setObjectName("nameLineEdit")      
        self.nameHorBox.addWidget(self.nameLineEdit)

        self.outerVertBox.addLayout(self.nameHorBox)
        self.outerVertBox.addStretch()

        self.setLayout(self.outerVertBox)

        # Context menu for blank space
        self.projectMenu = QtWidgets.QMenu()
        self.startupContextMenu = QtWidgets.QMenu("Startup")
        self.shutdownContextMenu = QtWidgets.QMenu("Shutdown")
        self.stateContextMenu = QtWidgets.QMenu("State")
        self.projectMenu.addMenu(self.startupContextMenu)
        self.projectMenu.addMenu(self.shutdownContextMenu)
        self.projectMenu.addMenu(self.stateContextMenu)

    def addProjectItem(self, configname):
        logging.debug("addProjectItem(): retranslateUi(): instantiated")
        if configname in self.projectItemNames:
            logging.error("addprojectItem(): Item already exists in tree: " + str(configname))
            return

        #self.projectItemNames[configname] = configTreeWidgetItem
        logging.debug("addprojectItem(): retranslateUi(): Completed")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ProjectWidget()
    ui.show()
    sys.exit(app.exec_())