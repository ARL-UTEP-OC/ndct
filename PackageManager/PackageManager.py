from ConfigurationManager.ConfigurationManager import ConfigurationManager
import zipfile
import os
import shutil

class PackageManager():
    def __init__(self, file_path, file_name, project_data_path):
        self.file_path = file_path
        self.file_name = file_name
        self.main_path = project_data_path
        self.zip_file = os.path.basename(file_path)
        self.new_extracted_dir = ""
        #self.tmpOutPath = ConfigurationManager.get_instance().read_config_abspath("PACKAGE", "TMP_DATA_PATH")

    def unzip(self):
        #copy .zip file to corresponding directory first
        shutil.copy(self.file_path, self.main_path)
        
        new_file_path = os.path.join(self.main_path, self.file_name)

        os.mkdir(new_file_path)
        os.chdir(self.main_path)
        
        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.main_path)

        #for next steps of import.. 
        self.new_extracted_dir = os.path.dirname(self.file_name)
        
        #once done, remove the zip file
        #keep only the extracted directory
        os.remove(self.zip_file)

        #change dir back
        og_path = os.path.dirname(self.main_path)
        os.chdir(og_path)

    def get_new_dir(self):
        return self.new_extracted_dir

    def copy_files(self):
        if os.path.isdir(self.file_path):
            #if is dir, copy whole directory
            shutil.copytree(self.file_path, self.main_path)
        else:
            shutil.copyfile(self.file_path, self.main_path)