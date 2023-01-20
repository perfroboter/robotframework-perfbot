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
#DEFAULT_LAST_N_RUNS = 5
DEFAULT_DATABASE = "robot-exec-times.db"
DEFAULT_STAT_FUNCTION = "avg"
DEFAULT_MODE_REPORT = "report"
MODE_BREAK_TEST = "break_test"


class PerfEvalResultModifier(ResultVisitor):
    ROBOT_LISTENER_API_VERSION = 2

    #TODO: Globales und Suite-Timeout aus Testfällen berücksichtigen
    def __init__(self, stat_func: str=DEFAULT_STAT_FUNCTION, 
        devn: float=DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS, 
       db_path: str=DEFAULT_DATABASE, mode: str=DEFAULT_MODE_REPORT):
        print("Prams",stat_func,devn,db_path,mode)
        self.stat_func = stat_func
        if not self.stat_func == DEFAULT_STAT_FUNCTION:
            raise NotImplementedError("Only Avg as statistical function supported yet.")
        self.max_deviation= devn
        self.mode = mode
        #self.last_n_runs = last_n_runs
        self.db_path = db_path
        self.persistenceService = Sqlite3PersistenceService(db_path)
        #TODO: Eingabewerte auf Gültigkeit prüfen, z. B. durch Enum of mode

    def start_suite(self, suite: TestSuite):
        self.perf_result_dict = {}
        if  not suite.suites:
            perf_stats = self.persistenceService.get_testsuite_stats(suite.longname)

            text: str = self._eval_and_to_string_perf_stats(suite.tests,perf_stats)
            suite.metadata["Performance Analysis"] = text

            self.persistenceService.store_many_testruns(suite.tests)

    def visit_test(self, test):
        if self.mode == MODE_BREAK_TEST:
            calced_devn = self.perf_result_dict[test.longname][2]
            if calced_devn >self.max_deviation*100:
                print("Calced: " + str(calced_devn) + " vs. Max: " + str(self.max_deviation))
                old_test_status = test.status
                test.status = 'FAIL'
                test.message = "PerfError: Test run lasted " + f'{calced_devn:.2f}' + " % than the average runs in the past and is thus above the maximum threshold of " + f'{self.max_deviation*100:.2f}' + " % (original test status was "+ str(old_test_status) + ")."




    def _eval_and_to_string_perf_stats(self, tests, perfstats): 
        text: str = "*Summary of Tests Performance*\n\n| =Testcase= |  =Elapsed=  | =Avg= | =Min= | =Max= | =Evaluated test runs= | =Deviation from avg= |\n"

        for t in tests:
            isInStats = False
            for ps in perfstats:
                if ps[0] == t.longname:
                    text+=  "| " + t.name + " | " + str(t.elapsedtime) + " | " + f'{ps[1]:.2f}' + " | " + str(ps[2]) + " | " + str(ps[3]) + " | " + str(ps[4])  + " | " + f'{100-ps[1]/t.elapsedtime*100:.2f}' + " % |\n"
                    self.perf_result_dict[t.longname] = ((t,ps,100-ps[1]/t.elapsedtime*100))
                    perfstats.remove(ps)
                    isInStats = True
                    break
            if not isInStats:
                    text+=  "| " + t.name + " | " + str(t.elapsedtime) + " | " + 'NO STATS' + " | " + 'NO STATS' + " | " + 'NO STATS' + " | " + 'NO STATS' + " | " + 'NO STATS'+  " |\n"
        return text