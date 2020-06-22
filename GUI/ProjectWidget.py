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

        self.setObjectName("ProjectWidget")
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().resizeSection(0, 150)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.outerVertBox.addWidget(self.treeWidget)

    def addProjectItem(self, configname):
        logging.debug("addProjectItem(): retranslateUi(): instantiated")
        if configname in self.projectItemNames:
            logging.error("addrojectItem(): Item already exists in tree: " + str(configname))
            return
        configTreeWidgetItem = QtWidgets.QTreeWidgetItem(self.treeWidget)
        configTreeWidgetItem.setText(0,configname)
        configTreeWidgetItem.setText(1,"Unknown")
        self.rojectItemNames[configname] = configTreeWidgetItem
        logging.debug("addrojectItem(): retranslateUi(): Completed")
    
    def showContextMenu(self, position):
        logging.debug("removeExperimentItem(): showContextMenu(): instantiated")
        self.experimentMenu.popup(self.treeWidget.mapToGlobal(position))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ProjectWidget()
    ui.show()
    sys.exit(app.exec_())