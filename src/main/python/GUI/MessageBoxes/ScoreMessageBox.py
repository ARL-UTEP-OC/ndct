import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ScoreMessageBox(QMessageBox):
   def __init__(self, displaytext):
      QMessageBox.__init__(self)
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      lay = QVBoxLayout(self.content)
      for line in displaytext.splitlines():
         lay.addWidget(QLabel(line, self))
      self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
      self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")
      self.showMaximized()
