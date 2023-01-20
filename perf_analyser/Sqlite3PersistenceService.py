#import PersistenceService
import sqlite3
from robot.result.model import TestCase, TestSuite

SQL_CREATE_TABLE_IF_NOT_EXISTS = "CREATE TABLE IF NOT EXISTS keywords_exec_times (id MEDIUMINT, starttime VARCHAR(255) NOT NULL, elapsedTime VARCHAR(255) NOT NULL, longname VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL,PRIMARY KEY (id));"
SQL_INSERT_TESTRUN = "INSERT INTO keywords_exec_times (starttime, elapsedTime, longname, status) VALUES (?, ?, ?, ?)"
SQL_SELECT_AVG_OF_LAST_RUNS = "SELECT AVG(elapsedTime) FROM (SELECT elapsedTime FROM keywords_exec_times WHERE longname = ? ORDER BY ID DESC LIMIT ?) AS TEMP;"

SQL_SELECT_STATS_OF_TESTSUITE = "SELECT longname, AVG(elapsedTime) as avg, MIN(elapsedTime) as min, MAX(elapsedTime) as max, count(elapsedTime) as count FROM (SELECT longname, elapsedTime FROM keywords_exec_times WHERE longname like ? ) AS TEMP GROUP BY longname;"
SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE = "SELECT * FROM keywords_exec_times WHERE longname like ? "

 #TODO: Idee der abstrakten Klasse erstmal verworfen, bei zweiter Persistenz-Möglichkeit nochmal anbinden class Sqlite3PersistenceService(PersistenceService):
class Sqlite3PersistenceService():

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute(SQL_CREATE_TABLE_IF_NOT_EXISTS)

    def store_testrun(self, test: TestCase):
        self.cur.execute(SQL_INSERT_TESTRUN, self._convert_robot_testresult_to_tabledata(test))
        self.con.commit()

    def store_many_testruns(self, tests):
        testruns = []
        for t in tests:
            testruns.append(self._convert_robot_testresult_to_tabledata(t))
        self.cur.executemany(SQL_INSERT_TESTRUN, testruns)
        self.con.commit()

    def _convert_robot_testresult_to_tabledata(self, test: TestCase):
         return (str(test.starttime), str(test.elapsedtime), str(test.longname), str(test.status))


    def get_last_n_runs(self, test_longname: str, n: int):
         raise NotImplementedError()

    def get_avg_of_last_runs(self, test_longname: str, last_n: int=5):
        self.cur.execute(SQL_SELECT_AVG_OF_LAST_RUNS, (test_longname, last_n))

        dbresult = self.cur.fetchone()

        return dbresult[0]

    #TODO: Limit auf Testfall einbauen?
    def get_testsuite_stats(self, suite_name):
        self.cur.execute(SQL_SELECT_STATS_OF_TESTSUITE, (str(suite_name + "%"),))

        return self.cur.fetchall()

    #TODO: Limit auf Testfall einbauen?
    def get_testsuite_testruns(self, suite_name):
        self.cur.execute(SQL_SELECT_ALL_TESTRUNS_OF_TESTSUITE, (str(suite_name + "%"),))

        return self.cur.fetchall()
