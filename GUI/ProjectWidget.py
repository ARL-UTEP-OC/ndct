from PyQt5 import QtCore, QtGui, QtWidgets
import logging

class ProjectWidget(QtWidgets.QWidget):

    def __init__(self):
        logging.debug("MaterialWidget instantiated")
        QtWidgets.QWidget.__init__(self, parent=None)

        self.setWindowTitle("ProjectWidget")
        self.setObjectName("ProjectWidget")

        self.outerVertBox = QtWidgets.QVBoxLayout()
        self.outerVertBox.setObjectName("outerVertBox")
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ProjectWidget()
    ui.show()
    sys.exit(app.exec_())