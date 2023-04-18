#import PersistenceService
import sqlite3
from PersistenceService import PersistenceService, Testrun, TestPerfStats, StoredTestrun, Keywordrun
from robot.result.model import TestCase, TestSuite
from typing import List

SQL_CREATE_TABLE_TESTS = "CREATE TABLE IF NOT EXISTS test_exec_times (id INTEGER, name TEXT NOT NULL, longname TEXT NOT NULL, starttime TEXT NOT NULL, elapsedTime INTEGER NOT NULL, status TEXT NOT NULL,PRIMARY KEY (id));"
SQL_CREATE_TABLE_KEYWORDS = "CREATE TABLE IF NOT EXISTS keyword_exec_times (id INTEGER, name TEXT NOT NULL, longname TEXT NOT NULL, testcase_longname TEXT NOT NULL, parent_keyword_longname TEXT, libname TEXT, starttime TEXT NOT NULL, elapsedTime INTEGER NOT NULL, status TEXT NOT NULL, keyword_level INT, counter INT, PRIMARY KEY (id));"
SQL_INSERT_TESTRUN = "INSERT INTO test_exec_times (name, longname, starttime, elapsedTime, status) VALUES (?, ?, ?, ?, ?)"
SQL_INSERT_KEYWORDS = "INSERT INTO keyword_exec_times (name, longname, testcase_longname, parent_keyword_longname, libname, starttime, elapsedTime, status, keyword_level, counter) VALUES (?, ?, ?, ?, ?,  ?, ?, ?, ?, ?)"

SQL_SELECT_STATS_OF_TESTSUITE = "SELECT name, longname, AVG(elapsedTime) as avg, MIN(elapsedTime) as min, MAX(elapsedTime) as max, count(elapsedTime) as count FROM (SELECT name, longname, elapsedTime FROM test_exec_times WHERE longname like ? AND status='PASS') AS TEMP GROUP BY longname;"
SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE = "SELECT * FROM test_exec_times WHERE longname like ? "

SQL_SELECT_STATS_OF_POSITIONAL_KEYWORDS = "SELECT name, longname, testcase_longname, parent_keyword_longname, libname, keyword_level, counter, avg(elapsedTime) as avg, min(elapsedTime) as min, max(elapsedTime) as max, count(elapsedTime) as count 	FROM keyword_exec_times WHERE testcase_longname like ? GROUP BY Testcase_longname, Longname, counter;"
SQL_SELECT_GLOBAL_KEYWORDS_STATS = "SELECT name, longname, testcase_longname, libname, avg(elapsedTime) as avg, min(elapsedTime) as min, max(elapsedTime) as max, count(elapsedTime) as count 	FROM keyword_exec_times WHERE testcase_longname like ? GROUP BY Longname;"

class Sqlite3PersistenceService(PersistenceService):
    """Persistierung der Testergebnisse erfolgt in einer lokalen Sqlite3-Datei.

    :param PersistenceService: Abstrakte Basisklasse, die die Methoden vorgibt.
    """

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute(SQL_CREATE_TABLE_TESTS)
        self.cur.execute(SQL_CREATE_TABLE_KEYWORDS)
    
    def insert_testrun(self, test):
        self.cur.execute(SQL_INSERT_TESTRUN, tuple(Testrun.from_robot_testCase(test)))
        self.con.commit()

    def insert_multiple_testruns(self, tests):
        testruns = []
        for t in tests:
            testruns.append(tuple(Testrun.from_robot_testCase(t)))
        self.cur.executemany(SQL_INSERT_TESTRUN, testruns)
        self.con.commit()

    def insert_multiple_keywords(self, keywords: List[Keywordrun]):
        self.cur.executemany(SQL_INSERT_KEYWORDS, keywords)
        self.con.commit()

    def select_testruns_by_testname(self, test_name, limit) -> List[StoredTestrun]:
        raise NotImplementedError()

    def select_multiple_testruns_by_suitename(self, suite_name) -> List[StoredTestrun]:
        self.cur.execute(SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE, (str(suite_name + "%"),))

        return self.cur.fetchall()

    def select_stats_grouped_by_suitename(self, suite_name) -> List[TestPerfStats]:
        self.cur.execute(SQL_SELECT_STATS_OF_TESTSUITE, (str(suite_name + "%"),))
        return self.cur.fetchall()

    def select_keyword_stats_grouped_by_run_order(self, suite_name):
        self.cur.execute(SQL_SELECT_STATS_OF_POSITIONAL_KEYWORDS, (str(suite_name + "%"),))
        return self.cur.fetchall()
    
    def select_global_keywords_stats_by_suitename(self, suite_name):
        self.cur.execute(SQL_SELECT_GLOBAL_KEYWORDS_STATS, (str(suite_name + "%"),))
        return self.cur.fetchall()






    
    
