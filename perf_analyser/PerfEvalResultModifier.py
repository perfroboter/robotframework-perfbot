# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-532
from robot.api import ResultVisitor
from robot.api.logger import info, debug, trace, console
import json, os.path
import sqlite3
from robot.result.model import TestCase, TestSuite
from Sqlite3PersistenceService import Sqlite3PersistenceService

# Constants
DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE = 10 # Sekunden
DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS = 1.0 # max 100% mehr (negative Angaben auch möglich)
DEFAULT_LAST_N_RUNS = 5
DEFAULT_DATABASE = "robot-exec-times.db"


class PerfEvalResultModifier(ResultVisitor):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, max_seconds: float=DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE, 
        max_deviation_from_last_runs: float=DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS, 
        last_n_runs: int=DEFAULT_LAST_N_RUNS, database: str=DEFAULT_DATABASE):
        self.max_execution_time = max_seconds * 1000
        self.max_deviation_from_last_runs= max_deviation_from_last_runs
        self.last_n_runs = last_n_runs
        self.database = database
        self.persistenceService = Sqlite3PersistenceService(database)
        self.listOfMessages = []
        self.listAsString = ""

        

    def visit_test(self, test: TestCase):
        # Relevanten Daten des Testfalls extrahieren und in die DB schreiben
        testcase_val = (str(test.starttime), str(test.elapsedtime), str(test.longname), str(test.status))
        self.persistenceService.store_testrun(testcase_val)
        
        avgOfLastNRuns = self.persistenceService.get_avg_of_last_runs(test.longname, self.last_n_runs)

        perf_result = {
            "Testcase":test.name,
            "":""
        }
        
        # Wenn Schwellwert erreicht Fehler auf FAIL setzen und Message in Report schreiben
        performance_metrics_msg = 'ElapsedTime=' + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs)
        info("Performance Report: ElapsedTime=" + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs))
        
        #TODO: Status des Testfalls berücksichtigen
        if test.elapsedtime > self.max_execution_time or test.elapsedtime > (avgOfLastNRuns*(1.0+self.max_deviation_from_last_runs)):
            test.status = 'FAIL'
            test.message = 'Performance Error: ' + performance_metrics_msg
        self.listAsString += "| " + test.name + " | " + str(test.elapsedtime) + " | " f'{avgOfLastNRuns}' + " | " + f'{100-test.elapsedtime/avgOfLastNRuns*100:.2f}' + " % |\n"

  

    def end_suite(self, suite: TestSuite):
        if  self.listAsString:
            text: str = "*Performanzanalyse*\n\n| =Testcase= |  =Elapsed=  | =Agv of last Runs=  | =Deviation= |\n"
            text+=self.listAsString
            suite.metadata["Performance Analysis"] = text
            self.listAsString = ""
