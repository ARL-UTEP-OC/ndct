import json
import logging
import os
import shutil
import shlex
import sys, traceback
import time
from jinja2 import Environment, FileSystemLoader
from subprocess import Popen
import subprocess
from collections import OrderedDict 
import random

class Scorer():
    
    def __init__(self):
        self.bins = OrderedDict()
        self.grouped_truepositive = OrderedDict()
        self.grouped_falsenegative = OrderedDict()
        self.grouped_falsepositive = OrderedDict()
        self.raw_alerts = ""
        self.total_TP = 0
        self.total_FP = 0
        self.total_FN = 0
        self.score_report = ""

    def extract_solutions_from_json(self, soln_filename):
        try:
            logging.debug("extract_solutions_from_json() instantiated")
            with open(soln_filename) as json_input:
                logging.debug("extract_solutions_from_json(): Reading comments")
                event_json = json.load(json_input)

            for event in event_json:
                logging.debug("Event: " + str(event))
                start_times = event["start-times"]
                for start_time in start_times:
                    self.bins[start_time] = {"found": False, "id": event["id"], "message_if_found": event["message-if-found"], "message_if_missed": event["message-if-missed"], \
                        "hints_if_missed": event["hints-if-missed"], "difficulty": event["difficulty"]}
            logging.debug("constructBinsFromJSON() Final Bins: " + str(self.bins))
            
            logging.debug("constructBinsFromJSON() Completed")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("extract_solutions_from_json(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

    def score_alerts(self, alerts_filename):
        logging.debug("score_alerts() instantiated")
        self.raw_alerts = ""
        self.total_TP = 0
        self.total_FP = 0
        self.total_FN = 0
        try:
            f = open(alerts_filename, "r")
            
            for line in f.readlines():
                split = line.split("[**]")
                if len(split) != 3:
                    continue
                (alert_time, msg, details) = split
                #check if there's a bin:
                alert_time = alert_time.strip()
                msg = msg.strip()
                details = details.strip()
                fromIP = details.split("} ")[1].split(" ")[0]
                toIP = fromIP = details.split("} ")[1].split(" ")[2]
                #Find matches (true positives)
                if alert_time in self.bins:
                    logging.debug("score_alerts() Found: " + alert_time)
                    #set to True
                    line = "CORRECT  FOUND: " + line
                    self.bins[alert_time]["found"] = True
                    self.total_TP +=1
                    #store id and a timestamps (only one needed since all share detailed JSON values)
                    if self.bins[alert_time]["id"] not in self.grouped_truepositive:
                        self.grouped_truepositive[self.bins[alert_time]["id"]] = alert_time    
                    logging.debug("write_results_to_file() Found: " + str(self.bins[alert_time]["message_if_found"]))
                #Otherwise its a false positive
                else:
                    logging.debug("score_alerts() NOT Found: " + alert_time)
                    #set to True
                    line = "FALSE POSITIVE: " + line
                    self.total_FP +=1
                    #store id and a timestamps (only one needed since all share detailed JSON values)
                    if alert_time not in self.grouped_falsepositive:
                        self.grouped_falsepositive[alert_time] = True
                    logging.debug("score_alerts() False Positive: " + str(alert_time))
                self.raw_alerts += line
            #Now go through and find the false negatives
            for alert_time in self.bins:
                if self.bins[alert_time]["found"] == False:
                    self.total_FN+=1
                    #store id and a timestamps (only one needed since all share detailed JSON values)
                    if self.bins[alert_time]["id"] not in self.grouped_falsenegative:
                        self.grouped_falsenegative[self.bins[alert_time]["id"]] = alert_time    
                    logging.debug("write_results_to_file() NOT Found: " + str(self.bins[alert_time]["message_if_missed"]))
            
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("score_alerts(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()
        
        logging.debug("score_alerts() Completed")

    def generate_results_report(self):
        logging.debug("generate_results_report() Instantiated")
        self.score_report = ""
        answer = ""

        # now store into string
        logging.debug("generate_results_report() Generating String Data.")
        great_job_text = """
************************************************************************
  _____                _    __          ______  _____  _  ___ 
 / ____|              | |   \ \        / / __ \|  __ \| |/ / |
| |  __ _ __ ___  __ _| |_   \ \  /\  / / |  | | |__) | ' /| |
| | |_ | '__/ _ \/ _` | __|   \ \/  \/ /| |  | |  _  /|  < | |
| |__| | | |  __/ (_| | |_     \  /\  / | |__| | | \ \| . \|_|
 \_____|_|  \___|\__,_|\__|     \/  \/   \____/|_|  \_\_|\_(_)
************************************************************************
"""           
        overall_score = int((float(self.total_TP*1.0)) / (float(self.total_TP) + float(self.total_FN)) * 100.0)
        if overall_score == 100:
            answer += great_job_text
        answer += "-----------------------------------RESULTS------------------------------------\r\n"
        answer += "------------------------------------------------------------------------------\r\n"
        answer += "--------------------------------OVERALL SCORE---------------------------------\r\n"
        answer += "                                   " + str(overall_score) + "% \r\n\r\n"
        answer += "--------------------------------FOUND INCIDENTS-------------------------------\r\n"
        answer += "\tTotal: " + str(self.total_TP) + " incidents from " + str(len(self.grouped_truepositive)) + " correctly commented packet(s).\r\n"
        answer += "------------------------------------------------------------------------------\r\n"
        answer += "--------------------------------MISSED INCIDENTS------------------------------\r\n"
        answer += "\tTotal: " + str(self.total_FN) + " incidents from " + str(len(self.grouped_falsenegative)) + " not commented packet(s).\r\n"
        answer += "------------------------------------------------------------------------------\r\n"
        answer += "---------------------------------FALSE POSITIVES------------------------------\r\n"
        answer += "\tTotal: " + str(self.total_FP) + " alerts resulting from incorrect comments or comments on wrong packet(s).\r\n\r\n\r\n"

        answer += "-----------------------------------DETAILS------------------------------------\r\n"
        answer += "------------------------------------------------------------------------------\r\n"
        answer += "-------------------FOUND INCIDENT TIMELINE (IN CHRONOLOGICAL ORDER)-----------\r\n"
        for item in self.bins:
            if self.bins[item]["found"] == True:
                answer += "TIME: " + item + ".." + self.bins[item]["message_if_found"] + "\r\n"

        answer += "------------------------------------------------------------------------------\r\n"
        answer += "------------------------------MISSING INCIDENTS-------------------------------\r\n"
        count = 1
        for item in self.grouped_falsenegative:
            #only need one time, because for the same id, they all have the same info
            atimestamp = self.grouped_falsenegative[item]
            answer += str(count) + ".\t" + self.bins[atimestamp]["message_if_missed"] + "..Difficulty: " + self.bins[atimestamp]["difficulty"] +"/5\r\n"
            count += 1
            randHintIndex = random.randrange(len(self.bins[atimestamp]["hints_if_missed"]))
            answer += "Hint: \t" + self.bins[atimestamp]["hints_if_missed"][randHintIndex] + "\r\n\r\n"
        answer += "\r\n\r\n"
        answer += "------------------------------------------------------------------------------\r\n"
        answer += "------------------------------RAW ALERT OUTPUT-------------------------------\r\n"
        for line in self.raw_alerts:
            answer += line
        
        logging.debug("generate_results_report() String generation complete.")
        logging.debug("generate_results_report() Completed.")
        self.score_report = answer
        return answer

    def get_score_report(self):
        return self.score_report

    def write_results_to_file(self, ofilename, score_data):
        logging.debug("write_results_to_file() Instantiated")
        try:
		    # now write output to a file
            logging.debug("write_results_to_file() File opened for writing: " + str(ofilename))
            resultsOF = open(ofilename, "w")
            logging.debug("write_results_to_file() Writing Rule Data to file.")
            resultsOF.write(score_data)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logging.error("write_results_to_file(): An error occured")
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            exit()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    if len(sys.argv) != 4:
        logging.error("Usage: compare_and_report_alerts.py <path-to-solutions-json> <path-to-submitted-alerts> <output-filename>")
        exit()
    soln_alerts_json = sys.argv[1]
    submitted_alerts = sys.argv[2]
    ofilename = sys.argv[3]
    scorer = Scorer()
    scorer.extract_solutions_from_json(soln_alerts_json)
    scorer.score_alerts(submitted_alerts)
    #generate the report:
    score_data = scorer.generate_results_report()
    scorer.write_results_to_file(ofilename, score_data)
    logging.debug("Program Complete")