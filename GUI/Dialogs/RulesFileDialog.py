from PyQt5.QtWidgets import QFileDialog, QWidget
import logging

class RulesFileDialog:
    def rules_dialog(self):
        logging.debug('rules_dialog(): Instantiated')
        widget = QFileDialog()
        filename = ""
        filename, _ = QFileDialog.getOpenFileNames(widget, "Choose a Rules file", "", "Rules Files (*.rules)")
        if len(filename) > 0:
            return filename[0]
        else:
            return ""
        logging.debug('rules_dialog(): Completed')