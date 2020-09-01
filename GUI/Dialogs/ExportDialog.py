from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QAction, QPushButton, QTextEdit, QMessageBox, QFileDialog, QSpacerItem
from PyQt5.QtCore import Qt
import logging
import os

from ConfigurationManager.FileExplorerRunner import FileExplorerRunner
from PackageManager.PackageManager import PackageManager
from GUI.Threading.BatchThread import BatchThread
from GUI.Dialogs.ProgressBarDialog import ProgressBarDialog

class ExportDialog(QtWidgets.QDialog):
    def __init__(self, parent, project_path, project_data_path):
        logging.debug("ExportDialog(): instantiated")
        super(ExportDialog, self).__init__(parent)
        self.parent = parent

        # quit = QAction("Quit", self)
        # quit.triggered.connect(self.closeEvent)
        # self.cancel_pressed = False

        self.project_path = project_path
        self.project_data_path = project_data_path

        #Title of window
        self.outerVertBoxPro = QtWidgets.QVBoxLayout()
        self.outerVertBoxPro.setObjectName("outerVertBox")
        self.setWindowTitle("Export Project")
        self.setObjectName("ExportProjectDialog")

        #Label - New Project Title
        self.labelVerBoxPro = QtWidgets.QVBoxLayout()
        self.labelVerBoxPro.setObjectName("labeVerBoxPro")
        self.newProjectLabel = QLabel("Exporting Project Settings")
        labelFont = QtGui.QFont()
        labelFont.setBold(True)
        self.newProjectLabel.setFont(labelFont)
        self.newProjectLabel.setAlignment(Qt.AlignCenter)
        self.labelVerBoxPro.addWidget(self.newProjectLabel)

        self.nameHorBox = QtWidgets.QHBoxLayout()
        self.nameHorBox.setObjectName("nameVerBoxPro")
        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Output Path:")
        self.nameHorBox.addWidget(self.nameLabel)

        self.exportOutputPath = QtWidgets.QLineEdit()
        self.exportOutputPath.setFixedWidth(200)
        self.exportOutputPath.setAcceptDrops(False)
        self.exportOutputPath.setReadOnly(True)
        self.exportOutputPath.setObjectName("exportOutputPath")
        self.nameHorBox.addWidget(self.exportOutputPath)

        self.exportPathButton = QPushButton("...")
        self.exportPathButton.clicked.connect(self.on_path_button_clicked)
        self.nameHorBox.addWidget(self.exportPathButton)

        self.exportPathViewButton = QPushButton("View")
        self.exportPathViewButton.clicked.connect(lambda x: self.on_view_button_clicked(x, self.exportOutputPath))
        self.nameHorBox.addWidget(self.exportPathViewButton)

        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.exportButton = QPushButton("Export")
        self.exportButton.setFixedWidth(60)
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(self.on_export_clicked)
        self.buttonsLayout.addWidget(self.exportButton)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedWidth(60)
        self.cancelButton.clicked.connect(self.on_cancel_button_clicked)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.buttonsLayout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.outerVertBoxPro.addLayout(self.labelVerBoxPro)
        self.outerVertBoxPro.addLayout(self.nameHorBox)
        #self.outerVertBoxPro.addLayout(self.spacer)
        self.outerVertBoxPro.addLayout(self.buttonsLayout)

        self.setFixedHeight(90)
        self.setFixedWidth(500)

        self.setLayout(self.outerVertBoxPro)

    def on_view_button_clicked(self, x, folder_path=None):
        if isinstance(folder_path, QTextEdit):
            folder_path = folder_path.toPlainText()
        elif isinstance(folder_path, QtWidgets.QLineEdit):
            folder_path = folder_path.text()
        if folder_path == "":
            QMessageBox.warning(self, 
                                "No path selected",
                                "There is no path selected",
                                QMessageBox.Ok)
            return None

        self.file_explore_thread = FileExplorerRunner(folder_location=folder_path)
        self.file_explore_thread.start()

    def on_path_button_clicked(self):
        logging.debug('on_log_out_path_button_clicked(): Instantiated')
        folder_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory to Store Data"))
        if folder_chosen == "":
            logging.debug("File choose cancelled")
            return
        self.exportOutputPath.setText(folder_chosen)
        self.exportButton.setEnabled(True)

    def on_export_clicked(self):
        out_path = self.exportOutputPath.text()
        #initialize package manager without any values in args
        package_mgr = PackageManager()
        zip_function = package_mgr.zip

        self.batch_thread = BatchThread()
        self.batch_thread.progress_signal.connect(self.update_progress_bar)
        self.batch_thread.completion_signal.connect(self.export_complete)
        self.batch_thread.add_function(zip_function, out_path, self.project_path, self.project_data_path)
        self.progress_dialog_overall = ProgressBarDialog(self, self.batch_thread.get_load_count())
        self.batch_thread.start()
        self.progress_dialog_overall.show()

    def update_progress_bar(self):
        logging.debug('update_progress_bar(): Instantiated')
        self.progress_dialog_overall.update_progress()
        logging.debug('update_progress_bar(): Complete')

    def export_complete(self):
        logging.debug("export_complete(): Instantiated")
        self.progress_dialog_overall.update_progress()      
        QMessageBox.information(self,
                            "Export Complete!",
                            "Success! Project Exported",
                            QMessageBox.Ok)
        self.progress_dialog_overall.hide()
        self.hide()
        logging.debug("copy_dir_complete(): Complete")

    def on_cancel_button_clicked(self, event):
        logging.debug('on_cancel_button_clicked(): Instantiated')
        self.hide()
        logging.debug('on_cancel_button_clicked(): Complete')

    def exec_(self):
        logging.debug("ExportDialog(): exec_() instantiated")
        result = super(ExportDialog, self).exec_()
        if str(result) == str(1):
            logging.debug("dialog_response(): OK was pressed")
            self.hide()
            return (QMessageBox.Ok)
        return (QMessageBox.Cancel)