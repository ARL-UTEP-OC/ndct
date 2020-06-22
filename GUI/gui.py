import logging
import sys
import os, traceback
import shutil
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
                QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, 
                QSpinBox, QAction, qApp, QStackedWidget, QMenuBar, QInputDialog,QFileDialog)

import time

from PyQt5.QtWidgets import QMessageBox

from GUI.baseWidget import BaseWidget
from GUI.ProjectWidget import ProjectWidget
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

class MainGUI(QMainWindow):

    def __init__(self, logman, comment_mgr, val):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__()
        self.setWindowTitle('Traffic Annotation Workflow')

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        mainlayout = QVBoxLayout()
        self.baseWidget = BaseWidget(logman, comment_mgr, val)
        self.projectWidget  = ProjectWidget()
        self.projectTree = QtWidgets.QTreeWidget()
        self.configname = ""
        #Temp - will change later
        self.existingconfignames = []
        self.baseWidgets = {}
        self.blankTreeContextMenu = {}
        
        quit = QAction("Quit", self)
        quit.triggered.connect(self.baseWidget.closeEvent)

        #Add tab widget - RES
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.setGeometry(QtCore.QRect(0, 15, 668, 565))
        tabWidget.setObjectName("tabWidget")

        #Configuration window - RES
        windowWidget = QtWidgets.QWidget()
        windowWidget.setObjectName("windowWidget")
        windowBoxHLayout = QtWidgets.QHBoxLayout()
        windowBoxHLayout.setObjectName("windowBoxHLayout")
        windowWidget.setLayout(windowBoxHLayout)

        self.projectTree.itemSelectionChanged.connect(self.onItemSelected)
        self.projectTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.projectTree.customContextMenuRequested.connect(self.showContextMenu)
        self.projectTree.setEnabled(True)
        self.projectTree.setMaximumSize(200,521)
        self.projectTree.setObjectName("projectTree")
        self.projectTree.headerItem().setText(0, "Projects")
        self.projectTree.setSortingEnabled(False)
        windowBoxHLayout.addWidget(self.projectTree)

        self.basedataStackedWidget = QStackedWidget()
        self.basedataStackedWidget.setObjectName("basedataStackedWidget")
        windowBoxHLayout.addWidget(self.basedataStackedWidget)
        tabWidget.addTab(windowWidget, "Configuration")

        #Add base info
        self.baseWidgets[self.configname] = {"BaseWidget": {}, "ProjectWidget": {} }
        self.baseWidgets[self.configname]["BaseWidget"] = self.baseWidget
        self.basedataStackedWidget.addWidget(self.baseWidget)

        #Set up context menu
        self.setupContextMenus()

        #ADD TAB WIDGET - RES
        self.initMenu()
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.mainMenu)
        mainlayout.addWidget(tabWidget)
        self.mainWidget.setLayout(mainlayout)

        logging.debug("MainWindow(): Complete")

    #RES Method
    def onItemSelected(self):
        logging.debug("MainApp:onItemSelected instantiated")
    	# Get the selected item
        selectedItem = self.projectTree.currentItem()
        if selectedItem == None:
            logging.debug("MainApp:onItemSelected no configurations left")
            self.statusBar.showMessage("No configuration items selected or available.")
            return
        # Now enable the save button
        #self.saveButton.setEnabled(True)
        self.saveProjectMenuButton.setEnabled(True)
        #Check if it's the case that an project name was selected
        parentSelectedItem = selectedItem.parent()
        if(parentSelectedItem == None):
            #A base widget was selected
            self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[selectedItem.text(0)]["ProjectWidget"])
        else:
            #Check if it's the case that a VM Name was selected
            if(selectedItem.text(0)[0] == "V"):
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentSelectedItem.text(0)]["VMWidgets"][selectedItem.text(0)]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentSelectedItem.text(0)]["VMWidgets"][selectedItem.text(0)])
            #Check if it's the case that a Material Name was selected
            elif(selectedItem.text(0)[0] == "M"):
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentSelectedItem.text(0)]["MaterialWidgets"][selectedItem.text(0)]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentSelectedItem.text(0)]["MaterialWidgets"][selectedItem.text(0)])

    #RES METHOD
    def setupContextMenus(self):
        logging.debug("MainApp:setupContextMenus() instantiated")
    # Context menu for blank space
        self.blankTreeContextMenu = QtWidgets.QMenu()
       	self.addproject = self.blankTreeContextMenu.addAction("New project")
       	self.addproject.triggered.connect(self.newProject)
        self.importproject = self.blankTreeContextMenu.addAction("Import project folder")
        self.importproject.triggered.connect(self.importActionEvent)

    #RES METHOD
    def showContextMenu(self, position):
    	logging.debug("MainApp:showContextMenu() instantiated: " + str(position))
    	if(self.projectTree.itemAt(position) == None):
    		self.blankTreeContextMenu.popup(self.projectTree.mapToGlobal(position))
    	elif(self.projectTree.itemAt(position).parent() == None):
    		self.projectContextMenu.popup(self.projectTree.mapToGlobal(position))
    	else:
    		self.itemContextMenu.popup(self.projectTree.mapToGlobal(position))

    #RES METHOD
    def initMenu(self):               
        
        self.mainMenu = QMenuBar()
        self.fileMenu = self.mainMenu.addMenu("File")

        self.newProjectMenuButton = QAction(QIcon(), "New Project", self)
        self.newProjectMenuButton.setShortcut("Ctrl+N")
        self.newProjectMenuButton.setStatusTip("Create New Project")
        self.newProjectMenuButton.triggered.connect(self.newProject)
        self.fileMenu.addAction(self.newProjectMenuButton)

        self.importProjectMenuButton = QAction(QIcon(), "Import Project", self)
        self.importProjectMenuButton.setShortcut("Ctrl+I")
        self.importProjectMenuButton.setStatusTip("Import folder")
        self.importProjectMenuButton.triggered.connect(self.importActionEvent)
        self.fileMenu.addAction(self.importProjectMenuButton)

        self.saveProjectMenuButton = QAction(QIcon(), "Save Project", self)
        self.saveProjectMenuButton.setShortcut("Ctrl+S")
        self.saveProjectMenuButton.setStatusTip("Save currently selected project")
        #self.saveProjectMenuButton.triggered.connect(self.saveProjectButton)
        self.saveProjectMenuButton.setEnabled(False)
        self.fileMenu.addAction(self.saveProjectMenuButton)
    
    #This method was added by:
    #Stephanie Medina
    #Used to create a new project, this is where the prompt to write a name for the project is taken.
    def newProject(self):
        #This path will be hardcoded temporaily. Will be changed later
        destinationPath = "data/"
        configname, ok = QInputDialog.getText(self, 'Project', 'Enter new project name \r\n(non alphanumeric characters will be removed)')
        if ok:
            #standardize and remove invalid characters
            self.configname = ''.join(e for e in self.configname if e.isalnum())
            self.existingconfignames += [configname]
            #check to make sure the name doesn't already exist
            if self.configname in self.existingconfignames:
                QMessageBox.warning(self.parent,
                                        "Name Exists",
                                        "The project name specified already exists",
                                        QMessageBox.Ok)            
                return None
        else:
            logging.debug("newProject(): Cancel was pressed")
            return

        #Call add project
        self.addProject(configname, destinationPath)

        return None

    #This method was added by:
    #Stephanie Medina
    #Used to create a new project, and this is where the project will actually be populated
    def addProject(self, filename, destinationPath):
        #create the folders and files for new project:
        self.filename = filename
        self.successfilenames = []
        self.successfoldernames = []
        self.destinationPath = destinationPath
        self.foldersToCreate = []
        self.filesToCreate = []
        basePath = os.path.join(destinationPath,filename)
        self.foldersToCreate.append(basePath)
        self.foldersToCreate.append(os.path.join(basePath, "Materials"))
        self.foldersToCreate.append(os.path.join(basePath, "Logs"))

        if filename != None:
            logging.debug("addProject(): OK pressed and valid configname entered: " + str(filename))
        
        configTreeWidgetItem = QtWidgets.QTreeWidgetItem(self.projectTree)
        configTreeWidgetItem.setText(0,filename)
        self.projectWidget.addProjectItem(filename)
            
        #add project widget and its contents
        self.baseWidgets[self.configname]["ProjectWidget"][filename] = self.projectWidget

        self.basedataStackedWidget.addWidget(self.projectWidget)
        self.basedataStackedWidget.addWidget(self.baseWidget)

    #A combination of RES Methods
    def importActionEvent(self):
        logging.debug("MainApp:importActionEvent() instantiated") 

        fdialog = QFileDialog()
        #Is there another way to get the files?
        #Would want to get a whole folder instead of just one file
        fdialog.setFileMode(QFileDialog.Directory)
        filenames = ""
        filenames, _ = QFileDialog.getOpenFileNames(fdialog, "Choose capture file to Import")
        if len(filenames) > 0:
            #check if experiment already exists
            filename = filenames[0]
            logging.debug("packageImportDialog(): files chosen: " + str(filename))
            baseNoExt = os.path.basename(filename)
            baseNoExt = os.path.splitext(baseNoExt)[0]
            self.configname = ''.join(e for e in baseNoExt if e.isalnum())
            #check to make sure the name doesn't already exist
            """ if self.configname in existingconfignames:
                QMessageBox.warning(self.parent,
                                        "Import Error",
                                        "An experiment with the same name already exists. Skipping...",
                                        QMessageBox.Ok)            
                return []           
            successfilenames = self.importData(filename)
            if len(successfilenames) > 0:
                logging.debug("packageImportDialog(): success files: " + str(successfilenames))
                successfilename = successfilenames[0]
                sbaseNoExt = os.path.basename(successfilename)
                sbaseNoExt = os.path.splitext(sbaseNoExt)[0]
                return sbaseNoExt """
        return []
    
    def quit_app(self):
        logging.debug("quit_app(): Instantiated()")
        self.destroy()
        self.quit_event.accept()
        qApp.quit()
        logging.debug("quit_app(): Completed()")
        return
