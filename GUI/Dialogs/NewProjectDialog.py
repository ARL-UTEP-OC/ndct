from PyQt5.QtWidgets import QInputDialog, QWidget, QMessageBox
from ConfigurationManager.ConfigurationManager import ConfigurationManager
import os
import logging

class ExperimentAddDialog:
    def experimentAddDialog(self, parent, existingconfignames):       
        logging.debug("experimentAddDialog(): Instantiated")
        self.parent = parent
        self.cm = ConfigurationManager()
        self.destinationPath = os.path.join(self.s.getConfig()['PROJECTS']['PROJECTS_BASE_PATH'])
        self.configname, ok = QInputDialog.getText(parent, 'Experiment', 
            'Enter new experiment name \r\n(non alphanumeric characters will be removed)')
        if ok:
            #standardize and remove invalid characters
            self.configname = ''.join(e for e in self.configname if e.isalnum())
            #check to make sure the name doesn't already exist
            if self.configname in existingconfignames:
                QMessageBox.warning(self.parent,
                                        "Name Exists",
                                        "The experiment name specified already exists",
                                        QMessageBox.Ok)            
                return None
            ##Otherwise, create the folders for this and return the name so that it can be added to the main GUI window
            successfilenames = self.addExperiment()
            logging.debug("experimentAddDialog(): Completed")
            if len(successfilenames) > 0:
                return self.configname
        return None

    def addExperiment(self):
        logging.debug("copyMaterial(): instantiated")
        #self.status = {"vmName" : self.vmName, "adaptorSelected" : self.adaptorSelected}
        #get the first value in adaptorSelected (should always be a number)
        status, successfoldernames, successfilenames = ExperimentAddingDialog(None, self.configname, self.destinationPath).exec_()
        return successfilenames