import logging
import os
import sys, traceback
import json
import time
from calendar import timegm
import shlex
from jinja2 import Environment, FileSystemLoader

class DissectorGenerator():

    def __init__(self, lua_scripts=None, pcap_filename=None):
        pass

    def getJSONFiles(self, folder_loc=None):
        logging.debug("getJSONFiles(): instantiated")
        #will hold the filenames
        filelist = list()
        try:
            if folder_loc:
                json_folder = folder_loc
            else:
                json_folder = os.path.join(os.getcwd(), './')
            logging.debug("getJSONFiles(): reading filenames")
            for r, d, f in os.walk(json_folder):
                for file in f:
                    if '.JSON' in file:
                        filelist.append(os.path.join(r, file))
            logging.debug("Found files: " + str(filelist))
            logging.debug("getJSONFiles(): File reading complete")
            return (filelist)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("readJSONData(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()	   

    #Read and extract data from JSON file
    def readJSONData(self, file_loc=None):
        logging.debug("readJSONData(): instantiated")
        #will hold the event and its timestamp
        eventlist = list()
        try:
            if file_loc:
                json_filename = file_loc
            else:
                json_filename = os.path.join(os.getcwd(), '2019_06_11Traffic_Curation_files/IV_snoopyData.JSON')
            logging.debug("readJSONData(): reading file as json data: " + str(json_filename))

            with open(json_filename, 'r') as json_file:
                data = json.load(json_file)
                for p in data:
                    if "content" not in p:
                        p['content'] = "Event Occured"
                    logging.debug("readJSONData(): appending: " + (str(p['content']) + " " + str(p['start']) + " " + str(timegm(time.strptime(str(p['start']), "%Y-%m-%dT%H:%M:%S")) ) ))
                    eventlist.append( (str(p['content']),str(p['start']), timegm(time.strptime(str(p['start']), "%Y-%m-%dT%H:%M:%S"))) )
            logging.debug("readJSONData(): File reading complete")
            return (eventlist)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("readJSONData(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()		
            
    def eventsToDissector(self, eventlist, dissector_name, start_threshold=0.1, end_threshold=1, template_filename=None, ofilename=None):
        logging.debug("eventsToDissector(): Instantiated")
        if template_filename == None:
            template_filename = "templates/timebased.jnj2"
        if ofilename == None:
            if os.path.exists("output-dissectors") == False:
                os.makedirs("output-dissectors")
            ofilename = "output-dissectors/" + dissector_name + ".lua"
        if ofilename.split(".")[-1] != "lua":
            ofilename += ".lua"
        
        eventlist_thresh = []
        #format the event and time in an easier to read format for the template
        for (event, time_date_tod, time_epoch) in eventlist:
            start_time = float(time_epoch) - start_threshold
            end_time = float(time_epoch) + end_threshold
            eventlist_thresh.append((start_time, end_time, time_date_tod, event))
    
        try:
            template_basename = os.path.basename(template_filename)

            env = Environment(
                loader=FileSystemLoader(os.path.dirname(template_filename))
                )
            logging.debug("eventsToDissector(): rendering " + ofilename + " using template: " + template_filename)
            
            with open(ofilename, "w") as out:
                #create the string from the template using the dissector_name, events, time, and thresholds
                out.write(env.get_template(template_basename).render(jinja_dissector_name = dissector_name, jinja_eventlist_thresh=eventlist_thresh))            

            logging.debug("Done creating dissector: " + os.path.abspath(ofilename))
            #return the (possibly modified) filename
            return ofilename

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("eventsToDissector(): An error occured ")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

if __name__=="__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level = logging.DEBUG)
    logging.debug("main(): Instantiated")
    dg = DissectorGenerator()
    filelist = dg.getJSONFiles("/root/git/eceld-netlabel/sample-logs/")
    file_events = {}
    dissector_filenames = []
    for filename in filelist:
        #save the filename as a key, all the events (event, time) as the value
        file_events = dg.readJSONData(filename)
        base = os.path.basename(filename)
        basenoext = os.path.splitext(base)[0]
        dissector_filename = dg.eventsToDissector(file_events, dissector_name=basenoext, ofilename="/root/git/eceld-netlabel/output-dissectors/"+basenoext, template_filename="/root/git/eceld-netlabel/templates/timebased.jnj2", start_threshold=0, end_threshold=2)
        dissector_filenames.append(dissector_filename)
    logging.debug("main(): Dissector Files Created: " + str(dissector_filenames))
    logging.debug("main(): Complete")