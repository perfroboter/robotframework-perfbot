import unittest
from ..Sqlite3PersistenceService import *
import os, glob
from robot.result import ExecutionResult
from robot.result.model import TestCase, TestSuite


# Beispieldaten entnommen aus: https://github.com/robotframework/robotframework/tree/master/utest/result
RESULT_1 = ExecutionResult(os.path.join(os.path.dirname(__file__), 'golden.xml'))
RESULT_2 = ExecutionResult(os.path.join(os.path.dirname(__file__), 'goldenTwice.xml'))



class TestSqlite3PersistenceService(unittest.TestCase):
    NAME_OF_TEST_DB = "perfbot_db_for_unittesting.db"

    def setUp(self):
        self.persistenceService: PersistenceService = Sqlite3PersistenceService(os.path.dirname(__file__) + "/" + self.NAME_OF_TEST_DB)
        self.assertIsNotNone(self.persistenceService)
        self.assertIsInstance(self.persistenceService, PersistenceService)

    def tearDown(self):
        f = os.path.dirname(__file__) + "/" + self.NAME_OF_TEST_DB
        os.remove(f)
        pass

    
    def test_insert_and_select_testcase(self):
        self.persistenceService.insert_test_execution("Test-Hostname")
        self.persistenceService.insert_testcase_run(RESULT_1.suite.tests[0])
        result = self.persistenceService.select_testcase_runs_filtered_by_testname(RESULT_1.suite.tests[0].longname)
        self.assertTrue(len(result) == 1)

    def test_multiple_insert_and_select_testcase(self):
        # Testdaten enthalten nur 1 Tesfall pro Suite
        suite: TestSuite = RESULT_2.suite
        self.persistenceService.insert_test_execution("Test-Hostname")
        self.persistenceService.insert_multiple_testcase_runs( suite.suites[0].tests)
        result = self.persistenceService.select_testcase_stats_filtered_by_suitename(suite.suites[0].longname)
        self.assertTrue(len(result) == 1)