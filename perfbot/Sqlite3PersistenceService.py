#import PersistenceService
import sqlite3
from PersistenceService import PersistenceService, Testrun, TestPerfStats
from robot.result.model import TestCase, TestSuite
from typing import List

SQL_CREATE_TABLE_IF_NOT_EXISTS = "CREATE TABLE IF NOT EXISTS test_exec_times (id INTEGER, name TEXT NOT NULL, longname TEXT NOT NULL, starttime TEXT NOT NULL, elapsedTime INTEGER NOT NULL, status TEXT NOT NULL,PRIMARY KEY (id));"
SQL_INSERT_TESTRUN = "INSERT INTO test_exec_times (name, longname, starttime, elapsedTime, status) VALUES (?, ?, ?, ?, ?)"

SQL_SELECT_STATS_OF_TESTSUITE = "SELECT name, longname, AVG(elapsedTime) as avg, MIN(elapsedTime) as min, MAX(elapsedTime) as max, count(elapsedTime) as count FROM (SELECT name, longname, elapsedTime FROM test_exec_times WHERE longname like ? ) AS TEMP GROUP BY longname;"
SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE = "SELECT * FROM test_exec_times WHERE longname like ? "

class Sqlite3PersistenceService(PersistenceService):

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute(SQL_CREATE_TABLE_IF_NOT_EXISTS)
    
    def insert_testrun(self, test):
        self.cur.execute(SQL_INSERT_TESTRUN, Testrun.from_robot_testCase(test).get_values_as_tuple())
        self.con.commit()

    def insert_multiple_testruns(self, tests):
        testruns = []
        for t in tests:
            testruns.append(Testrun.from_robot_testCase(t).get_values_as_tuple())
        self.cur.executemany(SQL_INSERT_TESTRUN, testruns)
        self.con.commit()

    def select_testruns_by_testname(self, test_name, limit) -> List[Testrun]:
        raise NotImplementedError()

    def select_multiple_testruns_by_suitename(self, suite_name) -> List[Testrun]:
        self.cur.execute(SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE, (str(suite_name + "%"),))

        return self.cur.fetchall()

    def select_stats_grouped_by_suitename(self, suite_name) -> List[TestPerfStats]:
        self.cur.execute(SQL_SELECT_STATS_OF_TESTSUITE, (str(suite_name + "%"),))
        return self.cur.fetchall()





    
    
