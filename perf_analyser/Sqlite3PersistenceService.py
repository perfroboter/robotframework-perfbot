#import PersistenceService
import sqlite3

SQL_CREATE_TABLE_IF_NOT_EXISTS = "CREATE TABLE IF NOT EXISTS keywords_exec_times (id MEDIUMINT, starttime VARCHAR(255) NOT NULL, elapsedTime VARCHAR(255) NOT NULL, longname VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL,PRIMARY KEY (id));"
SQL_INSERT_TESTRUN = "INSERT INTO keywords_exec_times (starttime, elapsedTime, longname, status) VALUES (?, ?, ?, ?)"
SQL_SELECT_AVG_OF_LAST_RUNS = "SELECT AVG(elapsedTime) FROM (SELECT elapsedTime FROM keywords_exec_times WHERE longname = ? ORDER BY ID DESC LIMIT ?) AS TEMP;"

 #TODO: Idee der abstrakten Klasse erstmal verworfen, bei zweiter Persistenz-Möglichkeit nochmal anbinden class Sqlite3PersistenceService(PersistenceService):
class Sqlite3PersistenceService():
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute(SQL_CREATE_TABLE_IF_NOT_EXISTS)

    def store_testrun(self, testcase):
        self.cur.execute(SQL_INSERT_TESTRUN, testcase)
        self.con.commit()

    def get_last_n_runs(self, test_longname: str, n: int):
         raise NotImplementedError()

    def get_avg_of_last_runs(self, test_longname: str, last_n: int=5):
        self.cur.execute(SQL_SELECT_AVG_OF_LAST_RUNS, (test_longname, last_n))

        dbresult = self.cur.fetchone()

        return dbresult[0]