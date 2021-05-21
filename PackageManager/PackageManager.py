from ConfigurationManager.ConfigurationManager import ConfigurationManager
import zipfile
import os, 
import sys, traceback
import shutil
import logging

class PackageManager():
    def __init__(self):
        logging.debug("PackageManager(): Instantiating")
        
    def unzip(self, zipfile_path, configname, project_data_path):
        logging.debug("PackageManager(): unzip(): Instantiating")
        try:                          
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
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("unzip(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def zip(self, output_path, project_name, project_data_path):
        logging.debug("PackageManager(): zip(): Instantiating")
        try:

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
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("zip(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def get_dir_components(self, project_data_path):
        logging.debug("PackageManager(): get_dir_components(): Instantiating")
        try:
            filePaths = []
            for root, directories, files in os.walk(project_data_path):
                for filename in files:
                    filePath = os.path.join(root, filename)
                    filePaths.append(filePath)
                del directories
            
            return filePaths
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("get_dir_components(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def copy_files(self, src, dst):
        logging.debug("PackageManager(): copy_files(): Instantiating")
        try:
            if os.path.isdir(src):
                #if is dir, copy whole directory
                self.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("copy_files(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def copytree(self, src, dst, symlinks=False, ignore=None):
        logging.debug("PackageManager(): copytree(): Instantiating")
        try:
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("copytree(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)