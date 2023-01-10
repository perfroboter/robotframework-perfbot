# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-536
import os.path
from robot.api.logger import info, debug, trace, console
import sqlite3

# Constants
DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE = 10 # Sekunden
DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS = 1.0 # max 10% mehr (negative Angaben auch möglich)
DEFAULT_LAST_N_RUNS = 5


class PythonListener: #ResultModifier
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, max_seconds: float=DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE, 
        max_deviation_from_last_runs: float=DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS, 
        last_n_runs: int=DEFAULT_LAST_N_RUNS):
        self.max_execution_time = max_seconds * 1000
        self.max_deviation_from_last_runs= max_deviation_from_last_runs
        self.last_n_runs = last_n_runs
        self.connect_to_database()
        self.listOfMessages = list()


    def end_test(self, data, test):
       # Relevanten Daten des Testfalls extrahieren und in die DB schreiben
        testcase_val = (str(test.starttime), str(test.elapsedtime), str(test.longname), str(test.status))
        self.insert_testcase_to_database(testcase_val)
        
        
        avgOfLastNRuns = self.get_avg_execution_time_from_database(test.longname, self.last_n_runs)
        
        # Wenn Schwellwert erreicht Fehler auf FAIL setzen und Message in Report schreiben

        performance_metrics_msg = 'ElapsedTime=' + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs)

        #TODO: Logging in den Testcase 
        info("Performance Report: ElapsedTime=" + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs))
        #TODO: Status des Testfalls berücksichtigen
        if test.elapsedtime > self.max_execution_time or test.elapsedtime > (avgOfLastNRuns*(1.0+self.max_deviation_from_last_runs)):
            test.status = 'FAIL'
            test.message = 'Performance Error: ' + performance_metrics_msg

        performance_metrics_msg+= 'Status=' + str(test.status)

        self.listOfMessages.append(test.name + ' ' + performance_metrics_msg)

    def connect_to_database(self):
        self.con = sqlite3.connect("robot-exec-times.db")
        self.dbcursor = self.con.cursor()

    def insert_testcase_to_database(self, testcase):
        sql = "INSERT INTO keywords_exec_times (starttime, elapsedTime, longname, status) VALUES (?, ?, ?, ?)"
        self.dbcursor.execute(sql, testcase)
        self.con.commit()
    
    def get_avg_execution_time_from_database(self, longname, last_n_runs):
        #TODO: Last_n_runs wird nicht genutzt
        sql = "SELECT AVG(elapsedTime) FROM (SELECT elapsedTime FROM keywords_exec_times WHERE longname = ? ORDER BY ID DESC LIMIT 5) AS TEMP;"
        val = (str(longname),)
        self.dbcursor.execute(sql, val)

        dbresult = self.dbcursor.fetchone()

        return dbresult[0]