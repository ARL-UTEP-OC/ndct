#This class is to keep track of 
#Project Name and its correlating session names

class ProjectSessions():
    def __init__(self):
        #create the list
        self.project = {}
        self.project[1] = {}
        self.at_start = True
        self.length = 0

    def add_project(self, project_name):
        if self.at_start == True:
            #start at 1
            self.project[1]
            self.project[1]["project_name"] = project_name
            #create session list for later use (if needed)
            self.project[1]["project_sessions"] = []
            self.at_start = False
            self.length += 1
            return
        else:
            #get length
            dic_len = self.get_length()
            new_id = dic_len + 1
            self.project[new_id] = {}
            self.project[new_id]["project_name"] = project_name
            #create session list for later use (if needed)
            self.project[new_id]["project_sessions"] = []
            self.length += 1
            return

    def add_project_session(self, project_name, project_session):
        p_id = self.get_project_id(project_name)

        #add session
        if project_session not in self.project[p_id]["project_sessions"]:
            self.project[p_id]["project_sessions"].append(project_session)
            #return true that sessions was added
            return True

        #return false for session not added
        #logging.debug("session: " + project_session + " already exists")
        return False
    
    def get_length(self):
        return self.length

    def print_d(self):
        logging.debug("WHOLE LIST: " + str(self.project))
        logging.debug("Broken Down List:")
        for p_id, p_info in self.project.items():
            logging.debug("\nProject ID: ", p_id)
            for key in p_info:
                logging.debug(key + ':', p_info[key])

    def get_project_id(self, project_name):
        #logging.debug("IN GET PROJECT ID:")
        #logging.debug("PROJECT NAME: " + project_name)
        for p_id, p_info in self.project.items():
            for key in p_info:
                if key == "project_name":
                    info = key + ":", p_info[key]
                    project = key + ":", project_name
                    #logging.debug(info)
                    if str(info) in str(project):
                        #logging.debug("PROJECT ID: " + str(p_id))
                        return p_id            

""" project_list = ProjectSessions()

project_list.add_project("t0")
logging.debug("FIRST PRINT")
project_list.print_d()
project_list.add_project("t1")
logging.debug("SECOND PRINT")
project_list.print_d()

logging.debug("ADD SESSIONS")
project_list.add_project_session("t0","sessionTest")
project_list.add_project_session("t0","sessionTest")
project_list.add_project_session("t1", "sessionTest")
logging.debug("AFTER ADDING FIRST SESSION")
project_list.print_d()
project_list.add_project_session("t0", "sessionTest2")
logging.debug("AFTER ADDING SECOND SESSION")

project_list.print_d() """