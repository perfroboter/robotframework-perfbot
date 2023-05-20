#import PersistenceService
import sqlite3
from .PersistenceService import PersistenceService, Testrun, TestPerfStats, StoredTestrun, Keywordrun
from robot.result.model import TestCase, TestSuite, Keyword
from typing import List
from os.path import dirname, join

SQL_CREATE_TABLES = "CREATE TABLE IF NOT EXISTS test_execution ( id integer PRIMARY KEY AUTOINCREMENT, imported_at text DEFAULT CURRENT_TIMESTAMP, hostname text ); CREATE TABLE IF NOT EXISTS testcase ( id integer PRIMARY KEY AUTOINCREMENT, name text, longname text, suitename text, UNIQUE(longname) ); CREATE TABLE IF NOT EXISTS keyword ( id integer PRIMARY KEY AUTOINCREMENT, name text, longname text, libname text, UNIQUE(longname) ); CREATE TABLE IF NOT EXISTS testcase_run ( id integer PRIMARY KEY AUTOINCREMENT, testcase_id integer REFERENCES testcase(id) ON DELETE CASCADE NOT NULL, test_execution_id integer REFERENCES test_execution(id) ON DELETE CASCADE NOT NULL, starttime text NOT NULL, elapsedtime text NOT NULL, status text NOT NULL ); CREATE TABLE IF NOT EXISTS keyword_run ( id integer PRIMARY KEY AUTOINCREMENT, testcase_run_id integer REFERENCES testcase_run(id) ON DELETE CASCADE NOT NULL, keyword_id integer REFERENCES keyword(id) ON DELETE CASCADE NOT NULL, starttime text NOT NULL, elapsedtime text NOT NULL, status text NOT NULL, keyword_level integer, stepcounter integer, parent_keyword_longname text ); CREATE VIEW IF NOT EXISTS testcase_run_view AS SELECT testcase.name, testcase.longname, testcase_run.starttime, testcase_run.elapsedtime, testcase_run.status, test_execution.id, test_execution.hostname FROM testcase_run INNER JOIN testcase ON testcase_run.testcase_id = testcase.id INNER JOIN test_execution ON testcase_run.test_execution_id = test_execution.id; CREATE VIEW IF NOT EXISTS keyword_run_view AS SELECT testcase.name as testcase_name, testcase.longname as testcase_longname, testcase.suitename, keyword.name as kw_name, keyword.longname as kw_longname, keyword.libname, keyword_run.starttime, keyword_run.elapsedtime, keyword_run.status, keyword_run.keyword_level, keyword_run.stepcounter, keyword_run.parent_keyword_longname, test_execution.id, test_execution.hostname FROM keyword_run INNER JOIN keyword ON keyword_run.keyword_id = keyword.id INNER JOIN testcase_run ON keyword_run.testcase_run_id = testcase_run.id INNER JOIN testcase ON testcase_run.testcase_id = testcase.id INNER JOIN test_execution ON testcase_run.test_execution_id = test_execution.id;"

SQL_INSERT_TEST_EXECUTION = "INSERT INTO test_execution (hostname) VALUES (?);"
SQL_SELECT_TEST_EXECUTION = "SELECT  max(id) FROM test_execution VALUES (?,?,?)"
SQL_INSERT_OR_IGNORE_TESTCASE = "INSERT OR IGNORE INTO testcase (name, longname, suitename) VALUES (?,?,?);"
SQL_INSERT_TESTCASE_RUN = "INSERT INTO testcase_run (testcase_id, test_execution_id, starttime, elapsedtime, status) VALUES ((SELECT id FROM testcase WHERE longname = ?), (SELECT max(id) FROM test_execution), ?, ?,?);"
SQL_INSERT_OR_IGNORE_KEYWORD = "INSERT OR IGNORE INTO keyword (name, longname, libname) VALUES (?,?,?)"
SQL_INSERT_KEYWORD_RUN = "INSERT INTO keyword_run (testcase_run_id, keyword_id, starttime, elapsedtime, status, keyword_level, stepcounter, parent_keyword_longname) VALUES ((SELECT max(testcase_run.id) FROM testcase_run INNER JOIN testcase ON testcase_run.testcase_id = testcase.id WHERE testcase.longname =?), (SELECT id FROM keyword WHERE keyword.longname = ?),?,?,?,?,?,?)"
SQL_SELECT_TESTCASE_RUNS_FILTERED_BY_TESTCASE = "SELECT id ,name, longname, starttime , elapsedtime , status FROM testcase_run_view WHERE longname = ?"
SQL_SELECT_TESTCASE_RUNS_FILTERED_BY_TESTSUITE = "SELECT id ,name, longname, starttime , elapsedtime , status FROM testcase_run_view WHERE longname LIKE ?"
SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_TESTCASE = "SELECT * FROM keyword_run_view WHERE testcase_longname = ?"
SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_POSITIONAL_KEYWORD = "SELECT * FROM keyword_run_view WHERE testcase_longname = ? and kw_longname= ? and stepcounter= ?"
SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_TESTSUITE = "SELECT * FROM keyword_run_view WHERE testcase_longname LIKE ?"
SQL_SELECT_TESTCASE_RUN_STATS_OF_TESTCASE = "SELECT name, longname, AVG(elapsedtime) as avg, MIN(elapsedtime) as min, MAX(elapsedtime) as max, count(elapsedtime) as count FROM  testcase_run_view WHERE longname = ?"
SQL_SELECT_TESTCASE_RUN_STATS_OF_TESTSUITE = "SELECT name, longname, AVG(elapsedtime) as avg, MIN(elapsedtime) as min, MAX(elapsedtime) as max, count(elapsedtime) as count FROM (SELECT * FROM testcase_run_view WHERE longname like ? AND status='PASS') AS TEMP GROUP BY longname;"
SQL_SELECT_KEYWORD_RUN_STATS_GLOBAL = "SELECT kw_name, kw_longname, libname, avg(elapsedtime) as avg, min(elapsedtime) as min, max(elapsedtime) as max, count(elapsedtime) as count FROM keyword_run_view GROUP BY kw_longname;"
SQL_SELECT_KEYWORD_RUN_STATS_POSITIONAL = "SELECT kw_name, kw_longname, testcase_longname, parent_keyword_longname, libname, keyword_level, stepcounter, avg(elapsedtime) as avg, min(elapsedtime) as min, max(elapsedtime) as max, count(elapsedtime) as count FROM keyword_run_view GROUP BY testcase_longname, kw_longname, stepcounter;"
SQL_SELECT_KEYWORD_RUN_STATS_POSITIONAL_FILTERED_BY_TESTCASE = "SELECT kw_name, kw_longname, testcase_longname, parent_keyword_longname, libname, keyword_level, stepcounter, avg(elapsedtime) as avg, min(elapsedtime) as min, max(elapsedtime) as max, count(elapsedtime) as count FROM keyword_run_view WHERE testcase_longname = ? GROUP BY testcase_longname, kw_longname, stepcounter;"

class Sqlite3PersistenceService(PersistenceService):
    """Persistierung der Testergebnisse erfolgt in einer lokalen Sqlite3-Datei.

    :param PersistenceService: Abstrakte Basisklasse, die die Methoden vorgibt.
    """

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        #TODO: Relevativer Pfad notwendig
       # with open(join(dirname(__file__), 'schema.sql', 'r') as sql_file:
        #    sql_script = sql_file.read()

        self.cur.executescript(SQL_CREATE_TABLES)
        self.con.commit()

    def insert_test_execution(self, host_name):
        #TODO: Get start- und endtime of testexecution
        self.cur.execute(SQL_INSERT_TEST_EXECUTION, (host_name,))
        self.con.commit()
    

    def insert_testcase_run(self, test: TestCase):
        #TODO: Only works if test_execution is inserted before / no multiuser insert
        self.cur.execute(SQL_INSERT_OR_IGNORE_TESTCASE, (test.name, test.longname, test.parent.name));
        self.cur.execute(SQL_INSERT_TESTCASE_RUN, (test.longname, test.starttime, test.elapsedtime, test.status));
        self.con.commit()

    def insert_multiple_testcase_runs(self, testruns):
        temp_cases = []
        temp_runs = []
        for t in testruns:
            temp_cases.append((t.name, t.longname, t.parent.name))
            temp_runs.append((t.longname, t.starttime, t.elapsedtime, t.status))
        self.cur.executemany(SQL_INSERT_OR_IGNORE_TESTCASE, temp_cases)
        self.cur.executemany(SQL_INSERT_TESTCASE_RUN, temp_runs)
        self.con.commit()

    def insert_keyword_run(self, keywordrun: Keywordrun):
        #TODO: Voraussetzung: letzter Testlauf des Testfall ist geinserted und hat höchste ID
        self.cur.execute(SQL_INSERT_OR_IGNORE_KEYWORD, (keywordrun.name, keywordrun.longname, keywordrun.libname))
        self.cur.execute(SQL_INSERT_KEYWORD_RUN, (keywordrun.testcase_longname,keywordrun.longname,keywordrun.starttime,keywordrun.elapsedTime,keywordrun.status, keywordrun.keyword_level,keywordrun.counter,keywordrun.parent_keyword_longname))
        self.con.commit()

    def insert_multiple_keyword_runs(self, keywordruns):
        temp_keywords = []
        temp_runs = []
        for keywordrun in keywordruns:
            temp_keywords.append((keywordrun.name, keywordrun.longname, keywordrun.libname))
            temp_runs.append((keywordrun.testcase_longname,keywordrun.longname,keywordrun.starttime,keywordrun.elapsedTime,keywordrun.status, keywordrun.keyword_level,keywordrun.counter,keywordrun.parent_keyword_longname))
        self.cur.executemany(SQL_INSERT_OR_IGNORE_KEYWORD, temp_keywords)
        self.cur.executemany(SQL_INSERT_KEYWORD_RUN, temp_runs)
        self.con.commit()

    def select_testcase_runs_filtered_by_testname(self, testcase_longname):
        self.cur.execute(SQL_SELECT_TESTCASE_RUNS_FILTERED_BY_TESTCASE, (str(testcase_longname),))
        return self.cur.fetchall()

    def select_testcase_runs_filtered_by_suitename(self, suite_longname):
        self.cur.execute(SQL_SELECT_TESTCASE_RUNS_FILTERED_BY_TESTSUITE, (str(suite_longname + "%"),))
        return self.cur.fetchall()
    
    def select_testcase_stats_filtered_by_testname(self, testcase_longname):
        self.cur.execute(SQL_SELECT_TESTCASE_RUN_STATS_OF_TESTCASE, (str(testcase_longname),))
        return self.cur.fetchall()
    
    def select_testcase_stats_filtered_by_suitename(self, suite_longname) -> List[TestPerfStats]:
        self.cur.execute(SQL_SELECT_TESTCASE_RUN_STATS_OF_TESTSUITE, (str(suite_longname + "%"),))
        return self.cur.fetchall()

    def select_keyword_runs_filtered_by_testname(self, testcase_longname):
        self.cur.execute(SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_TESTCASE, (str(testcase_longname),))
        return self.cur.fetchall()
    
    def select_keyword_runs_filtered_by_positional_keyword(self, testcase_longname, keyword_longname, stepcounter):
        self.cur.execute(SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_POSITIONAL_KEYWORD, (testcase_longname,keyword_longname, stepcounter))
        return self.cur.fetchall()

    def select_keyword_runs_filtered_by_suitename(self, suite_longname):
        self.cur.execute(SQL_SELECT_KEYWORD_RUNS_FILTERED_BY_TESTCASE, (str(suite_longname + "%"),))
        return self.cur.fetchall()
    
    def select_global_keyword_stats(self):
        self.cur.execute(SQL_SELECT_KEYWORD_RUN_STATS_GLOBAL)
        return self.cur.fetchall()


    def select_positional_keyword_stats(self, testcase_filter=None):
        if testcase_filter:
            self.cur.execute(SQL_SELECT_KEYWORD_RUN_STATS_POSITIONAL_FILTERED_BY_TESTCASE,(testcase_filter,))
            return self.cur.fetchall()
        else:
            self.cur.execute(SQL_SELECT_KEYWORD_RUN_STATS_POSITIONAL)
            return self.cur.fetchall()






    
    
