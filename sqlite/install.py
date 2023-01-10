import sqlite3

con = sqlite3.connect("robot-exec-times.db")

cur = con.cursor()
cur.execute("CREATE TABLE keywords_exec_times (id MEDIUMINT, starttime VARCHAR(255) NOT NULL, elapsedTime VARCHAR(255) NOT NULL, longname VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL,PRIMARY KEY (id));")
