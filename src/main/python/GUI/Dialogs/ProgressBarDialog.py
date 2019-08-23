from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QProgressBar

class ProgressBarDialog(QDialog):
    
    def __init__(self, parent, bar_length):
        super().__init__(parent)
        self.setModal(True)
        self.completed = 0
        self.setWindowTitle('Progress Dialog')
        self.setFixedSize(300, 100)
        # self.progress_bar(bar_length)

        mainlayout = QVBoxLayout()

        self.label4 = QLabel('Processing, please wait...')
        self.label4.setAlignment(Qt.AlignCenter)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(50, 40, 200, 20)
        self.progress.setMaximum(bar_length)
        
        mainlayout.addWidget(self.label4)
        mainlayout.addStretch()
        self.setLayout(mainlayout)

    def update_progress(self):
        self.completed += 1
        self.progress.setValue(self.completed)