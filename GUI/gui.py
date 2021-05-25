import sys
import logging
import os, traceback
import shutil
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5 import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
                QHBoxLayout, QLabel, QPushButton, QLineEdit, QProgressBar, QDoubleSpinBox, 
                QSpinBox, QAction, qApp, QStackedWidget, QMenuBar, QInputDialog, QFileDialog,
                QPlainTextEdit, QMessageBox)

import time
import re
from distutils.dir_util import copy_tree
from ConfigurationManager.ConfigurationManager import ConfigurationManager
from PackageManager.PackageManager import PackageManager

from GUI.Widgets.ProjectWidget import ProjectWidget
from GUI.Widgets.SessionWidget import SessionWidget
from GUI.Widgets.AnnotateWidget import AnnotateWidget
from GUI.Widgets.RulesWidget import RulesWidget
from GUI.Widgets.ResultsWidget import ResultsWidget
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog
from GUI.listProjectSessions import ProjectSessions
from GUI.Dialogs.ExportDialog import ExportDialog
from GUI.Dialogs.NewFromCollectDataDialog import NewFromCollectDataDialog
from GUI.Dialogs.NewFromPCAPDialog import NewFromPCAPDialog

class MainGUI(QMainWindow):
    def __init__(self, logman, comment_mgr, val):
        logging.debug("MainGUI(): Instantiated")
        super(MainGUI, self).__init__()
        self.setWindowTitle('Traffic Annotation Workflow')
        self.setFixedSize(670,565)

        self.logman = logman
        self.comment_mgr = comment_mgr
        self.val = val

        self.project_sessions = ProjectSessions()
        self.cm = ConfigurationManager.get_instance()

        #shared data between widgets
        self.existingconfignames = {}
        self.logEnabled = ''
        self.closeConfirmed = ''
        self.newProject_pressed = False
        self.newPro = None

        #get project folder
        self.project_data_folder = self.cm.read_config_value("PROJECTS", "PROJECTS_BASE_PATH")
        self.createRequiredSubDirectories()

        self.at_start = True

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        mainlayout = QVBoxLayout()
        self.baseWidget = QWidget() #BaseWidget()
        self.annotateWidget = QWidget()
        self.resultsWidget = QWidget()
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

        #ADD TAB WIDGET - RES
        self.initMenu()
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.mainMenu)
        mainlayout.addWidget(tabWidget)
        self.mainWidget.setLayout(mainlayout)

        #load any saved projects
        self.load_saved()
        self.load_sessions()
        self.at_start = False

        logging.debug("MainWindow(): Complete")

    def createRequiredSubDirectories(self):
        logging.debug("MainApp:createRequiredSubDirectories() instantiated")
        if os.path.exists(self.project_data_folder) == False:
            try:
                os.makedirs(self.project_data_folder)
            except:
                logging.error("MainApp:createRequiredSubDirectories(): An error occured when trying to create project directories: ")
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                QMessageBox.error(self,
                                        "Create Error",
                                        "Could not create project subdirectories, quitting...",
                                        QMessageBox.Ok) 
                exit()

    #RES Method
    def onItemSelected(self):
        logging.debug("MainApp:onItemSelected instantiated")
    	# Get the selected item
        self.selectedItem = self.projectTree.currentItem()
        if self.selectedItem == None:
            logging.debug("MainApp:onItemSelected no configurations left")
            self.statusBar.showMessage("No configuration items selected or available.")
            return
        #Check if it's the case that an project name was selected
        parentSelectedItem = self.selectedItem.parent()

        if(parentSelectedItem == None):
            #A base widget was selected
            #logging.debug"PROJECT_WIDGET: " + str((self.baseWidgets[self.selectedItem.text(0)]["ProjectWidget"])))
            self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[self.selectedItem.text(0)]["ProjectWidget"])
        else:
            #for children
            parentOfParent = parentSelectedItem.parent()

            #Check if it's the case that a Session Name was selected
            if(self.selectedItem.text(0)[0] == "S"):
                #logging.debug"SESSION_WIDGET: " + str(self.baseWidgets[parentSelectedItem.text(0)][self.selectedItem.text(0)]["SessionWidget"]))
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentSelectedItem.text(0)][self.selectedItem.text(0)]["SessionWidget"]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentSelectedItem.text(0)][self.selectedItem.text(0)]["SessionWidget"])
                #Check if it's the case that a Annotate was selected
            elif(self.selectedItem.text(0)[0] == "A"):
                #logging.debug"ANNOTATE " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["AnnotateWidget"]))
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["AnnotateWidget"]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["AnnotateWidget"])
            #Check if it's the case that a Rules was selected
            elif(self.selectedItem.text(0)[0] == "R"):
                #logging.debug"RULES " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["RulesWidget"]))
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["RulesWidget"]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["RulesWidget"])
            #Check if it's the case that a Results was selected
            elif(self.selectedItem.text(0)[0] == "X"):
                #logging.debug"RESULTS " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["ResultsWidget"]))
                logging.debug("Setting right widget: " + str(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["ResultsWidget"]))
                self.basedataStackedWidget.setCurrentWidget(self.baseWidgets[parentOfParent.text(0)][parentSelectedItem.text(0)]["ResultsWidget"])


    def on_add_curation_clicked(self):
        logging.debug("on_add_curation_clicked(): Instantiated")
        selectedItem = self.projectTree.currentItem()

        if selectedItem == None:
            QMessageBox.warning(self,
                                        "No Project Selected",
                                        "Could not add session, no project was selected",
                                        QMessageBox.Ok) 
        
        selectedItemName = selectedItem.text(0)

        sessionName, ok = QInputDialog.getText(self, 'New Session', 
            'Enter new session name \r\n(non alphanumeric characters will be removed)')
        if ok:
            sessionName = ''.join(e for e in sessionName if e.isalnum())
            if sessionName == '':
                QMessageBox.warning(self,
                                        "Invalid Name",
                                        "The session name specified is invalid",
                                        QMessageBox.Ok) 

            else: 
                add_session = self.add_session_list(selectedItemName, sessionName)
                if add_session == False:
                    QMessageBox.warning(self,
                                            "Session Name Exists",
                                            "The session name specified already exists",
                                            QMessageBox.Ok)    
                else:
                    sessionLabel = "S: " + sessionName
                    #create tree widget item
                    sessionItem = QtWidgets.QTreeWidgetItem(selectedItem)
                    sessionItem.setText(0,sessionLabel)   
                    sessionWidget = SessionWidget(sessionName)

                    self.baseWidgets[selectedItemName][sessionLabel] = {} #project name (Parent of Parent) + session name (parent of children)
                    self.baseWidgets[selectedItemName][sessionLabel]["SessionWidget"] = sessionWidget
                    self.basedataStackedWidget.addWidget(sessionWidget)

                    #create other widget items
                    ##ANNOTATE
                    annItem = QtWidgets.QTreeWidgetItem()
                    annLabel = "A: " + "Annotate"
                    annItem.setText(0, annLabel)
                    sessionItem.addChild(annItem)
                    self.annotateWidget = AnnotateWidget(self.project_data_folder, selectedItemName, os.path.basename(self.existingconfignames[selectedItemName]), sessionName, self.comment_mgr) #send project name for the corresponding directory

                    self.baseWidgets[selectedItemName][sessionLabel]["AnnotateWidget"] = self.annotateWidget #child
                    self.basedataStackedWidget.addWidget(self.annotateWidget)

                    ##RULES
                    rulesItem = QtWidgets.QTreeWidgetItem()
                    rulesLabel = "R: " + "Rules"
                    rulesItem.setText(0, rulesLabel)
                    sessionItem.addChild(rulesItem)
                    #add the corresponding directory -- if it is already created, skip
                    rulesDir = os.path.join(self.project_data_folder, selectedItemName)
                    rulesDir = os.path.join(rulesDir, "RULES")
    
                    if os.path.exists(rulesDir) == False:
                        os.mkdir(rulesDir)

                    rulesWidget = RulesWidget(self.project_data_folder, selectedItemName, os.path.basename(self.existingconfignames[selectedItemName]), sessionName, rulesDir, self.comment_mgr, self.val)

                    self.baseWidgets[selectedItemName][sessionLabel]["RulesWidget"] = rulesWidget
                    self.basedataStackedWidget.addWidget(rulesWidget)

                    ##RESULTS
                    resultsItem = QtWidgets.QTreeWidgetItem()
                    resultsLabel = "X: " + "Results"
                    resultsItem.setText(0, resultsLabel)
                    sessionItem.addChild(resultsItem)
                    #add the corresponding directory -- if it is already created, skip
                    resultsDir = os.path.join(self.project_data_folder, selectedItemName)
                    resultsDir = os.path.join(resultsDir, "IDS-ALERTS")
    
                    if os.path.exists(resultsDir) == False:
                        os.mkdir(resultsDir)
                
                    self.resultsWidget = ResultsWidget(self.project_data_folder, selectedItemName, sessionName, resultsDir, self.val)
               
                    self.baseWidgets[selectedItemName][sessionLabel]["ResultsWidget"] = self.resultsWidget
                    self.basedataStackedWidget.addWidget(self.resultsWidget)

        logging.debug("on_add_curation_clicked(): Completed")

    def on_export_clicked(self):
        #get project dir
        selectedItem = self.projectTree.currentItem()
        selectedItemName = selectedItem.text(0)

        project_folder = os.path.join(self.project_data_folder, selectedItemName)
        project_folder = os.path.abspath(project_folder)

        self.exportPro = ExportDialog(self, selectedItemName, project_folder).exec_()
        #self.exportPro.setWindowModality(QtCore.Qt.ApplicationModal)
        #self.exportPro.show()

    #RES METHOD
    def showContextMenu(self, position):
    	logging.debug("MainApp:showContextMenu() instantiated: " + str(position))
    	if(self.projectTree.itemAt(position) == None):
    		self.blankTreeContextMenu.popup(self.projectTree.mapToGlobal(position))
    	elif(self.projectTree.itemAt(position).parent() == None):
    		self.projectContextMenu.popup(self.projectTree.mapToGlobal(position))

    #RES METHOD
    def initMenu(self):               
        logging.debug("MainApp:initMenu() instantiated")
        self.mainMenu = QMenuBar()
        self.fileMenu = self.mainMenu.addMenu("File")

        self.blankTreeContextMenu = QtWidgets.QMenu()
       	self.newProjectContextMenu = QtWidgets.QMenu("New Project")
        self.blankTreeContextMenu.addMenu(self.newProjectContextMenu)

        self.fromCapture = self.newProjectContextMenu.addAction("Create Capture")
        self.fromCapture.triggered.connect(self.newFromCapture)

        self.fromPCAP = self.newProjectContextMenu.addAction("From PCAP")
        self.fromPCAP.triggered.connect(self.newFromPCAP)

        # Experiment context menu
        self.importContextMenu =  QtWidgets.QMenu("Import Project")
        self.blankTreeContextMenu.addMenu(self.importContextMenu)
        
        self.fromFolderContextSubMenu = self.importContextMenu.addAction("From Folder")
        self.fromFolderContextSubMenu.triggered.connect(self.importFromFolder)

        self.fromZipContextSubMenu = self.importContextMenu.addAction("From Zip")
        self.fromZipContextSubMenu.triggered.connect(self.importFromZip)

        #Context menu project 
        self.projectContextMenu = QtWidgets.QMenu()
        self.addCuration = self.projectContextMenu.addAction("Create curation session")
        self.addCuration.triggered.connect(self.on_add_curation_clicked)

        self.exportProject = self.projectContextMenu.addAction("Export project")
        self.exportProject.triggered.connect(self.on_export_clicked)

        self.quitAppMenuButton = QAction(QIcon(), "Quit", self)
        self.quitAppMenuButton.setShortcut("Ctrl+Q")
        self.quitAppMenuButton.setStatusTip("Quit App")
        self.quitAppMenuButton.triggered.connect(self.closeEvent)
        self.fileMenu.addAction(self.quitAppMenuButton)
    
    #Used to create a new project, this is where the prompt to write a name for the project is taken.
    def newFromCapture(self):
        logging.debug("MainApp:newFromCapture() instantiated")
        #Creating a custom widget to display what is needed for creating a new project:
        self.newPro = NewFromCollectDataDialog(self.logman, self.existingconfignames)
        #slots to receive data from the custom widget
        self.newPro.logEnabled.connect(self.log_enabled)
        self.newPro.created.connect(self.project_created)
        self.newPro.closeConfirmed.connect(self.close_confirmed)
        self.newProject_pressed = True
        self.newPro.setWindowModality(QtCore.Qt.ApplicationModal)
        self.newPro.show()

    def newFromPCAP(self):
        logging.debug("MainApp:newFromPCAP() instantiated")
        #Creating a custom widget to display what is needed for creating a new project:
        self.newCap = NewFromPCAPDialog(self.existingconfignames)
        #slot to receive data from the custom widget
        self.newCap.created.connect(self.project_created)
        self.newProject_pressed = True
        self.newCap.setWindowModality(QtCore.Qt.ApplicationModal)
        self.newCap.show()

    #Slot for when the user created the new project, path and configname
    @QtCore.pyqtSlot(str, dict, str)
    def project_created(self, configname, existingconfignames, path):
        #update project info with new info selected from widget     
        self.existingconfignames = existingconfignames
        #create the new project with the updated information
        self.addProject(configname, self.existingconfignames[configname], path)

    #Slot to let us know if the logging has started
    @QtCore.pyqtSlot(str)
    def log_enabled(self, status):
        self.logEnabled = status

    #Slot to let us know if the close has been confirmed or canceled
    @QtCore.pyqtSlot(str)
    def close_confirmed(self, status):
        self.closeConfirmed = status

    #Used to create a new project, and this is where the project will actually be populated
    def addProject(self, configname, projectPCAP, path):
        self.projectWidget  = ProjectWidget(configname, projectPCAP, path)
        #create the folders and files for new project:
        configTreeWidgetItem = QtWidgets.QTreeWidgetItem(self.projectTree)
        configTreeWidgetItem.setText(0,configname)
        self.projectWidget.addProjectItem(configname)

        #Add base info
        self.baseWidgets[configname] = {"BaseWidget": {}, "ProjectWidget": {}, "SessionWidget": {}, "AnnotateWidget": {}, "RulesWidget": {}, "ResultsWidget": {}}
        self.baseWidgets[configname]["BaseWidget"] = self.baseWidget
        self.basedataStackedWidget.addWidget(self.baseWidget)
        
        self.baseWidgets[configname]["ProjectWidget"] = self.projectWidget

        self.basedataStackedWidget.addWidget(self.projectWidget)
        self.basedataStackedWidget.addWidget(self.baseWidget)

        #add to list
        self.project_sessions.add_project(configname)

    def importFromZip(self):
        logging.debug("MainApp:importFromZip() instantiated") 
        zip_file = QFileDialog()
        zip_file.setWindowTitle("Select File")
        zip_file.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        zip_file.setNameFilter("Zip Files (*.zip)")

        filenames = zip_file.getOpenFileName()
        filename = filenames[0]
        if filename == "":
            logging.debug("File choose cancelled")
            return
        else:

            configname = os.path.basename(filename)
            configname = os.path.splitext(configname)[0]

            if configname in self.existingconfignames:
                QMessageBox.warning(self,
                                    "Name Exists",
                                    "A project with the same name already exists.",
                                    QMessageBox.Ok)            
                return None
            else:
                #instance of package manage
                pack_mgr = PackageManager()
                self.populate_import(pack_mgr, configname, os.path.abspath(filename))

    def importFromFolder(self, configname):
        logging.debug("MainApp:importFromFolder() instantiated") 

        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Store Data"))
        if folder_chosen == "":
            logging.debug("File choose cancelled")
            return

        if len(folder_chosen) > 0:
            baseNoExt = os.path.basename(folder_chosen)
            baseNoExt = os.path.splitext(baseNoExt)[0]
            configname = ''.join(e for e in baseNoExt if e.isalnum)
            if configname in self.existingconfignames:
                QMessageBox.warning(self,
                                    "Name Exists",
                                    "A project with the same name already exists.",
                                    QMessageBox.Ok)            
                return None
    
            else:
                self.populate_import("dir", configname, folder_chosen)

                
    def populate_import(self, function, configname, from_file):
        importedProjectPath = os.path.join(self.project_data_folder, configname)
        #copy selected dir to new dir
        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.copy_dir_complete)
        if function == "dir":
            self.batch_thread.add_function(self.copy_dir, from_file, importedProjectPath)

        else:
            self.batch_thread.add_function(function.unzip, from_file, configname, self.project_data_folder)

        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

    def load_project_widgets(self):
        logging.debug("load_project_widget(): loading project widget with saved projects")
        for name in self.existingconfignames:
            path = os.path.join(self.project_data_folder, name)
            projectPCAP = os.path.join(path, self.existingconfignames[name])
            configname = name
            self.addProject(configname, projectPCAP, path)
        logging.debug("load_project_widget(): Complete")

    def copy_dir(self, from_dir, to_dir):
        logging.debug("copy_dir(): copying selected directory")
        copy_tree(from_dir, to_dir)
        logging.debug("copy_dir(): copying complete")

    def copy_dir_complete(self):
        logging.debug("copy_dir_complete(): Instantiated")
        self.progress_dialog_overall.update_progress()
        self.progress_dialog_overall.hide()
        #Need to load projects (add to existing...)
        ##GET Project PCAP Name Here and also add to existingprojectnames
        self.load_saved()
        self.load_sessions()
        logging.debug("copy_dir_complete(): Complete")

    def load_saved(self):
        i = 0

        # #check if this is the project_pcap
        # for (dirName, subdirlist, filelist) in os.walk(path):
        #     for filename in filelist:
        #         spt = os.path.splitext(filename)
        #         if len(spt) > 0 and spt[1] == "pcap" or spt[1] == "pcapng":
        #             project_pcap_filename = filename
        #             break

        #for each subdir, import the saved projects
        for (dirName, subdirlist, filelist) in os.walk(self.project_data_folder):
            for projectFolder in subdirlist:
                pcapSubdir = os.path.join(self.project_data_folder, projectFolder, ConfigurationManager.STRUCTURE_PCAP_SUBDIR)
                abspcapSubdir = os.path.abspath(pcapSubdir)
                if os.path.exists(abspcapSubdir):
                    #go one level down
                    #if this is the pcap directory, then check if a pcap exists
                    #if so, this is a good project; create an entry in existingconfignames
                    for (subdirName, subsubdirlist, subfilelist) in os.walk(abspcapSubdir):
                        if len(subfilelist) == 1:
                            filename = subfilelist[0]
                            spt = os.path.splitext(filename)
                            if spt[1] == ".pcap" or spt[1] == ".pcapng":
                                self.existingconfignames[projectFolder] = filename
                                break
        #once everything has been added, populate widget
        self.load_project_widgets()

    def load_sessions(self):
        for name in self.existingconfignames:
            #for already saved project
            project_path = os.path.join(self.project_data_folder, name)
            project_pcap_session = os.path.join(project_path, ConfigurationManager.STRUCTURE_PCAP_SUBDIR)
            if os.path.exists(project_pcap_session):
                paths, dirs, files = next(os.walk(project_pcap_session))
                if len(dirs) > 0:
                    self.traverse_sessions(name, project_pcap_session)

    def traverse_sessions(self, project_name, path):
        #if RULES dir exists in project folder, then sessions exists
        i = 0

        for (dirName, subdirlist, filelist) in os.walk(path):
            for sessionName in subdirlist:
                if os.path.isfile(sessionName):
                    #skip
                    break
                
                elif self.add_session_list(project_name, sessionName) == True:
                    self.add_session_widgets(project_name, self.existingconfignames[project_name], sessionName)

    def add_session_widgets(self, project_name, project_pcap_filename, sessionName):
        sessionLabel = "S: " + sessionName
        #create tree widget item
        selectedItem = self.projectTree.findItems(project_name, Qt.Qt.MatchContains)
        sessionItem = QtWidgets.QTreeWidgetItem(selectedItem[0])
        sessionItem.setText(0,sessionLabel)   
        sessionWidget = SessionWidget(sessionName)
        
        self.baseWidgets[project_name][sessionLabel] = {} #project name (Parent of Parent) + session name (parent of children)
        self.baseWidgets[project_name][sessionLabel]["SessionWidget"] = sessionWidget
        self.basedataStackedWidget.addWidget(sessionWidget)

        #create other widget items
        ##ANNOTATE
        annItem = QtWidgets.QTreeWidgetItem()
        annLabel = "A: " + "Annotate"
        annItem.setText(0, annLabel)
        sessionItem.addChild(annItem)
        self.annotateWidget = AnnotateWidget(self.project_data_folder, project_name, project_pcap_filename, sessionName, self.comment_mgr) #send project name for the corresponding directory

        self.baseWidgets[project_name][sessionLabel]["AnnotateWidget"] = self.annotateWidget #child
        self.basedataStackedWidget.addWidget(self.annotateWidget)

        ##RULES
        rulesItem = QtWidgets.QTreeWidgetItem()
        rulesLabel = "R: " + "Rules"
        rulesItem.setText(0, rulesLabel)
        sessionItem.addChild(rulesItem)
        #add the corresponding directory -- if it is already created, skip
        rulesDir = os.path.join(self.project_data_folder, project_name)
        rulesDir = os.path.join(rulesDir, "RULES")

        if os.path.exists(rulesDir) == False:
            os.mkdir(rulesDir)
    
        self.rulesWidget = RulesWidget(self.project_data_folder, project_name, project_pcap_filename, sessionName, rulesDir, self.comment_mgr, self.val)

        self.baseWidgets[project_name][sessionLabel]["RulesWidget"] = self.rulesWidget
        self.basedataStackedWidget.addWidget(self.rulesWidget)

        ##RESULTS
        resultsItem = QtWidgets.QTreeWidgetItem()
        resultsLabel = "X: " + "Results"
        resultsItem.setText(0, resultsLabel)
        sessionItem.addChild(resultsItem)
        #add the corresponding directory -- if it is already created, skip
        resultsDir = os.path.join(self.project_data_folder, project_name)
        resultsDir = os.path.join(resultsDir, "IDS-ALERTS")

        if os.path.exists(resultsDir) == False:
            os.mkdir(resultsDir)
                
        self.resultsWidget = ResultsWidget(self.project_data_folder, project_name, sessionName, resultsDir, self.val)
               
        self.baseWidgets[project_name][sessionLabel]["ResultsWidget"] = self.resultsWidget
        self.basedataStackedWidget.addWidget(self.resultsWidget)
            
    def add_session_list(self, project_name, project_session):
        #method returns true if session was successfully added
        success = self.project_sessions.add_project_session(project_name, project_session)

        if success == False:
            #self.project_sessions.print_d()
            return False
        else:
            #self.project_sessions.print_d()
            return True

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
                                "Are you sure you want to quit?",
                                QMessageBox.Yes | QMessageBox.No)

            if close == QMessageBox.Yes:
                #call the delete data function from new project, just to make sure
                #everything has been cleared out
                if self.newProject_pressed == True:
                    if self.newPro != None:
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