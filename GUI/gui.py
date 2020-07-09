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
                QSpinBox, QAction, qApp, QStackedWidget, QMenuBar, QInputDialog, QFileDialog,
                QPlainTextEdit, QMessageBox)

import time
import re

from distutils.dir_util import copy_tree

from ConfigurationManager.ConfigurationManager import ConfigurationManager

from GUI.Widgets.ProjectWidget import ProjectWidget
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.Dialogs.NewProjectDialog import NewProjectDialog

class MainGUI(QMainWindow):

    def __init__(self, logman, comment_mgr, val):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__()
        self.setWindowTitle('Traffic Annotation Workflow')
        self.setFixedSize(670,565)

        self.logman = logman
        self.comment_mgr = comment_mgr
        self.val = val

        #shared data between widgets
        self.configname = ''
        self.path = ''
        self.existingconfignames = []
        self.annotatedPCAP = ''
        self.sessionName = ''
        self.existingSessionNames = []
        self.logEnabled = ''
        self.closeConfirmed = ''
        self.newProject_pressed = False
        self.project_data_folder = "/home/kali/eceld-netsys/ProjectData"
        self.folder_chosen = ''
        self.at_start = True

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        mainlayout = QVBoxLayout()
        self.baseWidget = QWidget() #BaseWidget()
        self.projectTree = QtWidgets.QTreeWidget()
        self.baseWidgets = {}
        self.blankTreeContextMenu = {}
        
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        #Add tab widget - RES
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.setGeometry(QtCore.QRect(0, 15, 668, 565))
        tabWidget.setObjectName("tabWidget")

        #BaseWidget
        self.baseWidget.setWindowTitle("BaseWidget")
        self.baseWidget.setObjectName("BaseWidget")
        baseLayoutWidget = QtWidgets.QWidget()
        baseLayoutWidget.setObjectName("layoutWidget")
        self.baseOuterVertBox = QtWidgets.QVBoxLayout()
        self.baseOuterVertBox.setObjectName("outerVertBox")
        baseLayoutWidget.setLayout(self.baseOuterVertBox)

        self.baseWidget.setLayout(self.baseOuterVertBox)

        #Configuration window - RES
        ## windowBoxHLayout contains:
        ###projectTree (Left)
        ###basedataStackedWidget (Right)
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

        #Set up context menu
        self.setupContextMenus()

        #ADD TAB WIDGET - RES
        self.initMenu()
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.mainMenu)
        mainlayout.addWidget(tabWidget)
        self.mainWidget.setLayout(mainlayout)

        #load any saved projects
        self.load_saved()
        self.at_start = False

        logging.debug("MainWindow(): Complete")

    #RES Method
    def onItemSelected(self):
        logging.debug("MainApp:onItemSelected instantiated")
    	# Get the selected item
        self.selectedItem = self.projectTree.currentItem()
        if self.selectedItem == None:
            logging.debug("MainApp:onItemSelected no configurations left")
            self.statusBar.showMessage("No configuration items selected or available.")
            return
        # Now enable the save button
        self.saveProjectMenuButton.setEnabled(True)

        #Check if it's the case that an project name was selected
        parentSelectedItem = self.selectedItem.parent()
        if(parentSelectedItem == None):
            #A base widget was selected
            #print("PROJECT_WIDGET: " + str((self.baseWidgets[self.selectedItem.text(0)]["ProjectWidget"])))
            self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[self.selectedItem.text(0)]["ProjectWidget"])
        else:
            #Check if it's the case that a VM Name was selected
            if(self.selectedItem.text(0)[0] == "V"):
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentSelectedItem.text(0)]["VMWidgets"][self.selectedItem.text(0)]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentSelectedItem.text(0)]["VMWidgets"][self.selectedItem.text(0)])
            #Check if it's the case that a Material Name was selected
            elif(self.selectedItem.text(0)[0] == "M"):
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentSelectedItem.text(0)]["MaterialWidgets"][self.selectedItem.text(0)]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentSelectedItem.text(0)]["MaterialWidgets"][self.selectedItem.text(0)])

    #RES METHOD
    def setupContextMenus(self):
        logging.debug("MainApp:setupContextMenus() instantiated")
        #Context menu for blank space
        self.blankTreeContextMenu = QtWidgets.QMenu()
       	self.addproject = self.blankTreeContextMenu.addAction("New project")
       	self.addproject.triggered.connect(self.newProject)
        self.importproject = self.blankTreeContextMenu.addAction("Import project folder")
        self.importproject.triggered.connect(self.importActionEvent)

        #Context menu project 
        self.projectContextMenu = QtWidgets.QMenu()
        self.addCuration = self.projectContextMenu.addAction("Add Curation")
        self.addCuration.triggered.connect(self.on_add_curation_clicked)

    def on_add_curation_clicked(self):
        logging.debug("on_add_curation_clicked(): Instantiated")

        ok = QInputDialog.getText(self, 'New Session', 
            'Enter new session name \r\n(non alphanumeric characters will be removed)')
        if ok:
            self.sessionName = ''.join(e for e in self.sessionName if e.isalnum())
            if self.sessionName in self.existingSessionNames:
                QMessageBox.warning(self,
                                        "Session Name Exists",
                                        "The session name specified already exists",
                                        QMessageBox.Ok)    
            else:
                #if all good, add session name to list
                self.existingSessionNames += [self.sessionName]    

        logging.debug("on_add_curation_clicked(): Completed")

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

        self.quitAppMenuButton = QAction(QIcon(), "Quit", self)
        self.quitAppMenuButton.setShortcut("Ctrl+Q")
        self.quitAppMenuButton.setStatusTip("Quit App")
        self.quitAppMenuButton.triggered.connect(self.closeEvent)
        self.fileMenu.addAction(self.quitAppMenuButton)
    
    #Used to create a new project, this is where the prompt to write a name for the project is taken.
    def newProject(self):
        #Creating a custom widget to display what is needed for creating a new project:
        self.newPro = NewProjectDialog(self.logman, self.existingconfignames)
        #slots to receive data from the custom widget
        self.newPro.logEnabled.connect(self.log_enabled)
        self.newPro.created.connect(self.project_created)
        self.newPro.closeConfirmed.connect(self.close_confirmed)
        self.newProject_pressed = True
        self.newPro.show()

    #Slot for when the user created the new project, path and configname
    @QtCore.pyqtSlot(str, list, str, str)
    def project_created(self, configname, existingconfignames, pcap, path):
        #update project info with new info selected from widget
        self.configname = configname
        self.path = path
        self.existingconfignames = existingconfignames
        self.annotatedPCAP = pcap
        #create the new project with the updated information
        self.addProject()

    #Slot to let us know if the logging has started
    @QtCore.pyqtSlot(str)
    def log_enabled(self, status):
        self.logEnabled = status

    #Slot to let us know if the close has been confirmed or canceled
    @QtCore.pyqtSlot(str)
    def close_confirmed(self, status):
        self.closeConfirmed = status

    #Used to create a new project, and this is where the project will actually be populated
    def addProject(self):
        self.projectWidget  = ProjectWidget(self.configname, self.annotatedPCAP, self.path)
        #create the folders and files for new project:
        self.filename = self.configname

        if self.filename != None:
            logging.debug("addProject(): OK pressed and valid configname entered: " + str(self.filename))
        
        configTreeWidgetItem = QtWidgets.QTreeWidgetItem(self.projectTree)
        configTreeWidgetItem.setText(0,self.filename)
        self.projectWidget.addProjectItem(self.filename)

        #Add base info
        self.baseWidgets[self.configname] = {"BaseWidget": {}, "ProjectWidget": {} }
        self.baseWidgets[self.configname]["BaseWidget"] = self.baseWidget
        self.basedataStackedWidget.addWidget(self.baseWidget)
        
        self.baseWidgets[self.configname]["ProjectWidget"] = self.projectWidget

        self.basedataStackedWidget.addWidget(self.projectWidget)
        self.basedataStackedWidget.addWidget(self.baseWidget)

    def importActionEvent(self):
        logging.debug("MainApp:importActionEvent() instantiated") 
        
        if self.at_start == False:
            self.folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Store Data"))

        if self.folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(self.folder_chosen) > 0:
            baseNoExt = os.path.basename(self.folder_chosen)
            baseNoExt = os.path.splitext(baseNoExt)[0]
            self.configname = ''.join(e for e in baseNoExt if e.isalnum)
            if self.configname in self.existingconfignames:
                QMessageBox.warning(self,
                                        "Name Exists",
                                        "A project with the same name already exists.",
                                        QMessageBox.Ok)            
                return None
            else:
                self.existingconfignames += [self.configname]
                importedProjectPath = os.path.join(self.project_data_folder, self.configname)
                #copy selected dir to new dir
                self.batch_thread = BatchThread()
                self.batch_thread.progress_signal.connect(self.update_progress_bar)
                self.batch_thread.completion_signal.connect(self.copy_dir_complete)
                self.batch_thread.add_function(self.copy_dir, importedProjectPath)

                self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
                self.batch_thread.start()
                self.progress_dialog_overall.show()

                self.path = importedProjectPath
                self.annotatedPCAP = os.path.join(importedProjectPath, ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
                self.addProject()
        
    def load_project_widget(self):
        logging.debug("load_project_widget(): loading project widget with saved projects")
        for name in self.existingconfignames:
            self.path = os.path.join(self.project_data_folder, name)
            print(self.path)
            self.annotatedPCAP = os.path.join(self.path, ConfigurationManager.STRUCTURE_ANNOTATED_PCAP_FILE)
            self.configname = name
            self.addProject()
        logging.debug("load_project_widget(): Complete")

    def copy_dir(self, importPath):
        logging.debug("copy_dir(): copying selected directory")
        copy_tree(self.folder_chosen, importPath)
        logging.debug("copy_dir(): copying complete")

    def copy_dir_complete(self):
        logging.debug("copy_dir_complete(): Instantiated")
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        logging.debug("copy_dir_complete(): Complete")

    def load_saved(self):
        i = 0
        #for each subdir, import the saved projects
        for (dirName, subdirlist, filelist) in os.walk(self.project_data_folder):
            folders = ', '.join(subdirlist)
            folder = folders.strip().split(", ")
            num_folders_left = len(folder)

            #check if there is anything to import - is it empty?
            if folder[i] == '':
                #return if there's nothing to import
                break

            while(num_folders_left != 0):
                #add the saved projects to existing list
                self.existingconfignames += [folder[i]]             
                num_folders_left -= 1
                i += 1

            if(num_folders_left == 0):
                #once number of folders left reaches 0, stop the directory traversal
                break

            del filelist #needed only to traverse directory
            del dirName #needed only to traverse directory
        
        #once everything has been added, populate widget
        self.load_project_widget()
            
    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def closeEvent(self, event):
        logging.debug("closeEvent(): instantiated")

        self.quit_event = event

        if self.logEnabled == "TRUE":
            #This means that the new project widget is still running so call the close event
            #for that widget first to stop logger
            self.newPro.closeEvent(event)

            #Check if the close was confirmed or not
            if self.closeConfirmed == "TRUE":
                #after that's done, make sure to quit the app
                self.quit_event.accept()
                #self.close()
                qApp.quit()
            else: 
                return
        else:
            close = QMessageBox.question(self, 
                                "QUIT",
                                "Are you sure you want to quit? \n Any unsaved data will be lost",
                                QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                #call the delete data function from new project, just to make sure
                #everything has been cleared out
                if self.newProject_pressed == True:
                    self.newPro.delete_data()
                qApp.quit()
                return
            elif close == QMessageBox.No and not type(self.quit_event) == bool:
                    self.quit_event.ignore()
            pass
        return
        
    def quit_app(self):
        self.quit_event.accept()
        qApp.quit()
        return
            
        
                