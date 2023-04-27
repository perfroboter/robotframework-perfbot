import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
from Sqlite3PersistenceService import *
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

    

    def test_insert_multiple_and_select_multiple_with_one(self):
        self.persistenceService.insert_multiple_testruns(RESULT.suite.tests)

        result_list = self.persistenceService.select_multiple_testruns_by_suitename(RESULT.suite.name)

        self.assertTrue(len(result_list) == 1)
        result: StoredTestrun = result_list.pop()
        self.assertIsInstance(result, StoredTestrun) #TODO: Fix that return type is List of Testrun
        self.assertTupleEqual(Testrun.from_robot_testCase(RESULT.suite.tests[0]),result) #TODO: Fix that id is an parameter

    def test_insert_one_and_select_multiple(self):

        inserted_testcase = RESULT.suite.tests[0]
        self.persistenceService.insert_testrun(inserted_testcase)

        result_list = self.persistenceService.select_multiple_testruns_by_suitename(RESULT.suite.name)

        self.assertTrue(len(result_list) == 1)
        #TODO: Vergleich durch gleiche Objekte ermöglichen (s. o.)
    

    def test_stats_with_one(self):
        self.persistenceService.insert_multiple_testruns(RESULT.suite.tests)
        result_list: List[TestPerfStats] = self.persistenceService.select_stats_grouped_by_suitename(RESULT.suite.name)
        print(len(result_list))
        self.assertTrue(len(result_list) == 1)
        first: TestPerfStats = result_list.pop()
       # self.assertIsInstance(first,TestPerfStats)
        self.assertTrue(first.name == RESULT.suite.tests[0][0])
        self.assertTrue(RESULT.suite.tests[0][5] == 1)

        self.persistenceService.insert_multiple_testruns(RESULT.suite.tests)
        result_list: List[TestPerfStats] = self.persistenceService.select_stats_grouped_by_suitename(RESULT.suite.name)
        self.assertTrue(len(result_list) == 1)
        first: TestPerfStats = result_list[0]
        #TODO: test more arguments
        # self.assertIsInstance(first,TestPerfStats) # TODO: Fix type errors
       # self.assertTrue(first.name == RESULT.suite.tests[0].name)
       # self.assertTrue(first.count == 2)
        self.assertTrue(first.name == RESULT.suite.tests[0][0])
        self.assertTrue(RESULT.suite.tests[0][5] == 1)




        
