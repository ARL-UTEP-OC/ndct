from ConfigurationManager.ConfigurationManager import ConfigurationManager
import zipfile
import os
import shutil

class PackageManager():
    def __init__(self):
        self.file_path = ''
        self.file_name = ''
        self.main_path = ''
        self.zip_file = ''
        self.new_extracted_dir = ''
        
    def unzip(self, file_path, file_name, project_data_path):
        self.file_path = file_path
        self.file_name = file_name
        self.main_path = project_data_path
        if file_path != None:
            self.zip_file = os.path.basename(file_path)
        
        #copy .zip file to corresponding directory first
        path_to_selected = os.path.dirname(os.path.realpath(self.file_path))
        os.chdir(path_to_selected)
        self.copy_files(self.zip_file, self.main_path)
        
        os.chdir(self.main_path)
        new_file_path = os.path.join(self.main_path, self.file_name)

        os.mkdir(new_file_path)
        
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

    def zip(self, output_path, project_to_compress, project_data_path):
        self.main_path = project_data_path
        
        dir_comp = self.get_dir_components(project_to_compress)

        for fileName in dir_comp:
            print(fileName)

        #create the zip file in the chosen output path
        os.chdir(output_path)
        zipf = zipfile.ZipFile(project_to_compress+'.zip', 'w')

        #copy files to chosen output path
        new_dir = os.path.join(output_path, project_to_compress)
        os.mkdir(new_dir)
        os.chdir(self.main_path)
        self.copy_files(project_to_compress, new_dir)
        
        with zipf:
            for file in dir_comp:
                zipf.write(file)

        #remove the copied directory and keep only the .zip file
        dir_to_rm = os.path.join(output_path, project_to_compress)
        shutil.rmtree(dir_to_rm)

        #once done, change dir back
        og_path = os.path.dirname(self.main_path)
        os.chdir(og_path)

    def get_dir_components(self, dirname):
        #go to the projects folder to get path
        os.chdir(self.main_path)
        filePaths = []
        print("DIR: " + dirname)
        path = os.path.dirname(dirname)
        print("Path: " + path)
        for root, directories, files in os.walk(dirname):
            for filename in files:
                filePath = os.path.join(root, filename)
                filePaths.append(filePath)
            del directories

        print(filePaths)
        
        return filePaths

    def get_new_dir(self):
        return self.new_extracted_dir

    def copy_files(self, src, dst):
        if os.path.isdir(src):
            #if is dir, copy whole directory
            self.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)