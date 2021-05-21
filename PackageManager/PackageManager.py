from ConfigurationManager.ConfigurationManager import ConfigurationManager
import zipfile
import os
import shutil
import logging

class PackageManager():
    def __init__(self):
        logging.debug("PackageManager(): Instantiating")
        
    def unzip(self, zipfile_path, configname, project_data_path):
        logging.debug("PackageManager(): unzip(): Instantiating")
        if zipfile_path == None or os.path.exists(zipfile_path) == False:
            logging.error("Could not unzip because path was not specified or does not exist.")
            return

        outpath = os.path.join(project_data_path, configname)
        if os.path.exists(outpath) == False:
            os.mkdir(outpath)
        else:
            logging.error("Could not unzip because config with same name already exists: " + str(configname))
            return
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(outpath)

    def zip(self, output_path, project_name, project_data_path):
        logging.debug("PackageManager(): zip(): Instantiating")

        output_filename = os.path.join(output_path, str(project_name)+".zip")
        dir_comp = self.get_dir_components(project_data_path)

        #create the zip file in the chosen output path
        zipf = zipfile.ZipFile(output_filename, 'w')

        #now zip the files       
        with zipf:
            for file in dir_comp:
                logging.debug("FILE PATH: " + str(file))
                outfile = file[len(project_data_path):]
                logging.debug("zipping file: " + str(file) + " as " + str(outfile))
                zipf.write(file, arcname=outfile)

    def get_dir_components(self, project_data_path):
        logging.debug("PackageManager(): get_dir_components(): Instantiating")
        filePaths = []
        for root, directories, files in os.walk(project_data_path):
            for filename in files:
                filePath = os.path.join(root, filename)
                filePaths.append(filePath)
            del directories
        
        return filePaths

    def copy_files(self, src, dst):
        logging.debug("PackageManager(): copy_files(): Instantiating")
        if os.path.isdir(src):
            #if is dir, copy whole directory
            self.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    def copytree(self, src, dst, symlinks=False, ignore=None):
        logging.debug("PackageManager(): copytree(): Instantiating")
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)