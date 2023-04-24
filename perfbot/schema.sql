CREATE TABLE IF NOT EXISTS test_execution (
    id integer PRIMARY KEY AUTOINCREMENT,
    imported_at text DEFAULT CURRENT_TIMESTAMP,
    hostname text
);

CREATE TABLE IF NOT EXISTS testcase (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text,
    longname text,
    suitename text,
    UNIQUE(longname)
);

CREATE TABLE IF NOT EXISTS keyword (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text,
    longname text,
    libname text,
    UNIQUE(longname)
);

CREATE TABLE IF NOT EXISTS testcase_run (
    id integer PRIMARY KEY AUTOINCREMENT,
    testcase_id integer REFERENCES testcase(id) ON DELETE CASCADE NOT NULL,
    test_execution_id integer REFERENCES test_execution(id) ON DELETE CASCADE NOT NULL,
    starttime text NOT NULL,
    elapsedtime text NOT NULL,
    status text NOT NULL
);

CREATE TABLE IF NOT EXISTS keyword_run (
    id integer PRIMARY KEY AUTOINCREMENT,
    testcase_run_id integer REFERENCES testcase_run(id) ON DELETE CASCADE NOT NULL,
    keyword_id integer REFERENCES keyword(id) ON DELETE CASCADE NOT NULL,
    starttime text NOT NULL,
    elapsedtime text NOT NULL,
    status text NOT NULL,
    keyword_level integer,
    stepcounter integer,
    parent_keyword_longname text
);

CREATE VIEW IF NOT EXISTS testcase_run_view AS
SELECT testcase.name, testcase.longname, testcase_run.starttime, testcase_run.elapsedtime, testcase_run.status, test_execution.id, test_execution.hostname
FROM testcase_run
INNER JOIN testcase ON testcase_run.testcase_id = testcase.id
INNER JOIN test_execution ON testcase_run.test_execution_id = test_execution.id;


CREATE VIEW IF NOT EXISTS keyword_run_view AS
SELECT testcase.name as testcase_name, testcase.longname as testcase_longname, testcase.suitename, keyword.name as kw_name, keyword.longname as kw_longname, keyword.libname, keyword_run.starttime, keyword_run.elapsedtime, keyword_run.status, keyword_run.keyword_level, keyword_run.stepcounter, keyword_run.parent_keyword_longname, test_execution.id, test_execution.hostname
FROM keyword_run
INNER JOIN keyword ON keyword_run.keyword_id = keyword.id
INNER JOIN testcase_run ON keyword_run.testcase_run_id = testcase_run.id
INNER JOIN testcase ON testcase_run.testcase_id = testcase.id
INNER JOIN test_execution ON testcase_run.test_execution_id = test_execution.id;