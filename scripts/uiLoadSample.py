from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('eceld-netsys.ui', self)
        
        self.logOutPathButton.clicked.connect(self.printButtonPressed)
        self.show()

    def printButtonPressed(self):
        # This is executed when the button is pressed
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()