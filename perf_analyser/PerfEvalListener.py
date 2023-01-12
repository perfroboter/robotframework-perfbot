# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-536
import os.path
from robot.api.logger import info, debug, trace, console
import sqlite3
from Sqlite3PersistenceService import Sqlite3PersistenceService

# Constants
DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE = 10 # Sekunden
DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS = 1.0 # max 10% mehr (negative Angaben auch möglich)
DEFAULT_LAST_N_RUNS = 5
DEFAULT_DATABASE = "robot-exec-times.db"


class PerfEvalListener: #ResultModifier
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, max_seconds: float=DEFAULT_MAX_EXECUTION_TIME_OF_TESTCASE, 
        max_deviation_from_last_runs: float=DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS, 
        last_n_runs: int=DEFAULT_LAST_N_RUNS, database: str=DEFAULT_DATABASE):
        self.max_execution_time = max_seconds * 1000
        self.max_deviation_from_last_runs= max_deviation_from_last_runs
        self.last_n_runs = last_n_runs
        self.database = database
        self.persistenceService = Sqlite3PersistenceService(database)


    def start_test(self, test, result):
        test.body.create_keyword(name='Log', args=['Keyword added by listener! Insert <b>Boxplot</b> here <img src="example_result.png">', 'HTML'])

    def end_test(self, data, test):
       # Relevanten Daten des Testfalls extrahieren und in die DB schreiben
        testcase_val = (str(test.starttime), str(test.elapsedtime), str(test.longname), str(test.status))
        self.persistenceService.store_testrun(testcase_val)
        
        
        avgOfLastNRuns = self.persistenceService.get_avg_of_last_runs(test.longname, self.last_n_runs)
        
        # Wenn Schwellwert erreicht Fehler auf FAIL setzen und Message in Report schreiben

        performance_metrics_msg = 'ElapsedTime=' + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs)

        #TODO: Logging in den Testcase 
        info("Performance Report: ElapsedTime=" + str(test.elapsedtime) + " AvgOfLastNRuns=" + str(avgOfLastNRuns) + " MaxExecutionTime=" + str(self.max_execution_time) + " MaxDeviation=" + str(self.max_deviation_from_last_runs) + " N=" + str(self.last_n_runs))
        #TODO: Status des Testfalls berücksichtigen
        if test.elapsedtime > self.max_execution_time or test.elapsedtime > (avgOfLastNRuns*(1.0+self.max_deviation_from_last_runs)):
            test.message = 'Performance Error: ' + performance_metrics_msg + ' FunctionalTestStatus=' + test.status
            test.status = 'FAIL'