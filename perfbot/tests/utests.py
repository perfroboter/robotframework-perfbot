import unittest
from ..Sqlite3PersistenceService import *
import os, glob
from robot.result import ExecutionResult


# Beispieldaten entnommen aus: https://github.com/robotframework/robotframework/tree/master/utest/result
RESULT = ExecutionResult(os.path.join(os.path.dirname(__file__), 'golden.xml'))



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
        self.persistenceService.insert_testcase_run(RESULT.suite.tests[0])
        result = self.persistenceService.select_testcase_runs_filtered_by_testname(RESULT.suite.tests[0].longname)
        print(len(result))
        self.assertTrue(len(result) == 1)
        print(type(result.pop()))
        print(result)

    def test_insert_and_select_multiple_testcases(self):
        pass
