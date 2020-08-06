from PyQt5.QtWidgets import QInputDialog, QWidget, QMessageBox, QFileDialog
from PyQt5 import QtWidgets
from gui.Dialogs.PackageActioningDialog import PackageActioningDialog
import os
import logging

class ExportProjectDialog(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)

        fdialog = QFileDialog()
        fdialog.setFileMode(QFileDialog.DirectoryOnly)
        fdialog.setOption(QFileDialog.ShowDirsOnly, True)
        fdialog.setViewMode(QFileDialog.Detail)

        choosen_dirs, _ = QFileDialog.getOpenFileNames(fdialog, "Choose Export Folder")

        if len(choosen_dirs) < 0:
            logging.debug("File choose cancelled")
            return
        
        if len(choosen_dirs) > 0:
            filedir = choosen_dirs[0]
            
