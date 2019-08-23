from PyQt5.QtWidgets import QFileDialog, QWidget
import logging

class WiresharkFileDialog:
    def wireshark_dialog(self):
        logging.debug('wireshark_dialog(): Instantiated')
        widget = QFileDialog()
        filename = ""
        filename, _ = QFileDialog.getOpenFileNames(widget, "Choose a Wireshark file", "", "Wireshark Files (*.pcapng)")
        if len(filename) > 0:
            return filename[0]
        else:
            return ""
        logging.debug('wireshark_dialog(): Completed')