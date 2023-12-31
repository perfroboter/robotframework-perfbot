# see https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-532
from robot.api import ResultVisitor
from robot.api.logger import info, debug, trace, console   
import os
from datetime import datetime
from robot.result.model import TestSuite, Body, Keyword
from .PersistenceService import PersistenceService
from .Sqlite3PersistenceService import Sqlite3PersistenceService
from .PerfEvalVisualizer import PerfEvalVisualizer
from .model import JoinedPerfTestResult, Keywordrun
from typing import List
import socket

# Constants
DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS = 1.0 
DEFAULT_LAST_N_RUNS = None
DEFAULT_DATABASE_TECHNOLOGY = "sqlite3" 
DEFAULT_DATABASE_PATH = "robot-exec-times.db"
DEFAULT_BOXPLOT_FOLDER_REL_PATH = "perfbot-graphics/"
DEFAULT_STAT_FUNCTION = "avg" 
TEXT_PERF_ANALYSIS_TABLE_HEADING = "*Summary of Tests Performance*\n\n| =Testcase= |  =Elapsed=  | =Avg= | =Min= | =Max= | =Evaluated test runs= | =Deviation from avg= |\n"
TEXT_PERF_ANALYSIS_TABLE_ROW =  "| {name}  | {elapsedtime}  | {avg} | {min} | {max} | {count} | {devn} % |\n" 
TEXT_PERF_ANALYSIS_BOXPLOT = ""
TEXT_PERF_ANALYSIS_FOOTNOTE = ""
TEXT_PERF_ERROR_MESSAGE = "PerfError: Test run lasted {calced_devn:.2f} % than the average runs in the past and is thus above the maximum threshold of {max_devn:.2f} % (original test status was {old_test_status})."


class PerfEvalResultModifier(ResultVisitor):
    """Diese Klasse übernimmt die eigentliche Verarbeitungslogik nach dem Aufruf durch rebot oder von robot mit der Option prerebotmodifier.
    
    :class ResultVisitor: Basisklasse aus der robot.api von der diese Klasse erbt, welche das Iterieren über die Testergebnisse ermöglicht.
    :raises NotImplementedError: Einige Parameter sind nur mit default-Werten zulässig.
    """
    ROBOT_LISTENER_API_VERSION = 2

   
    perf_results_list_of_testsuite: List[JoinedPerfTestResult] = []

    body_items_of_testsuite = []

    #TODO: Globales und Suite-Timeout aus Testfällen berücksichtigen
    def __init__(self, stat_func: str=DEFAULT_STAT_FUNCTION, 
        devn: float=DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS, last_n_runs: int=DEFAULT_LAST_N_RUNS, db: str=DEFAULT_DATABASE_TECHNOLOGY,
       db_path: str=DEFAULT_DATABASE_PATH, boxplot: bool=True, boxplot_folder: str=DEFAULT_BOXPLOT_FOLDER_REL_PATH, testbreaker:bool=False, readonly=False, keywordstats:bool=True):
        """Es sind keine Parameter für den Aufruf nötig. Es lässt sich aber eine Vielzahl von Einstellung über folgende Parameter vornehmen:

        :param stat_func: Angabe, welche statistische Funktion zur Auswertung genutzt wird, defaults to DEFAULT_STAT_FUNCTION
        :type stat_func: str, optional
        :param devn: Angabe, ab welcher prozentualen Abweichung der Testbreaker auslösen soll, defaults to DEFAULT_MAX_DEVIATION_FROM_LAST_RUNS
        :type devn: float, optional
        :param last_n_runs: Angabe, wie viele letzten Testergebnisse analysierte werden, defaults to DEFAULT_LAST_N_RUNS
        :type last_n_runs: int, optional
        :param db: Angabe, welches Persistenz-Variante bzw. Datenbank genutzt wird, defaults to DEFAULT_DATABASE_TECHNOLOGY
        :type db: str, optional
        :param db_path: Angabe, wo die Datenbank gespeichert ist, defaults to DEFAULT_DATABASE_PATH
        :type db_path: str, optional
        :param boxplot: Angabe, ob die Historie der Testlaufzeiten in einem Boxplot grafisch aufbereitet werden soll, defaults to True
        :type boxplot: bool, optional
        :param boxplot_folder: Ordner, wo die referenzierten Bilder abliegen, defaults to DEFAULT_BOXPLOT_FOLDER_REL_PATH
        :type boxplot_folder: str, optional
         :param testbreaker: Angabe, ob Testfälle bei schlechter Performanz (abhängig von devn) auf FAIL gesetzt werden sollen, defaults to False
        :type testbreaker: bool, optional
        :param readonly: Angabe, ob nur lesend auf die persitierten Daten zugegriffen werden soll, defaults to False
        :type readonly: bool, optional
        :param keywordstats: Angabe, ob die Schlüsselwort-Ebene persistiert werden soll, defaults to True
        :type keywordstats: bool, optional
         :raises NotImplementedError: Einige Parameter (stat_func, last_n_runs, db) sind nur mit default-Werten zulässig und somit nicht veränderbar.
        """
        self.stat_func = stat_func
        if not self.stat_func == DEFAULT_STAT_FUNCTION:
            raise NotImplementedError("Only Avg as statistical function supported yet.")

        self.max_deviation= devn
        
        self.last_n_runs = last_n_runs
        if not self.last_n_runs == DEFAULT_LAST_N_RUNS:
            raise NotImplementedError("No limit supported yet.")
        
        self.db_technology = db
        if not self.db_technology == DEFAULT_DATABASE_TECHNOLOGY:
            raise NotImplementedError("Only Sqlite3 as database technology supported yet.")
        self.db_path = db_path
        self.persistenceService: PersistenceService = Sqlite3PersistenceService(db_path)

        self.boxplot_activated = boxplot
        if  self.boxplot_activated:
            self.visualizer = PerfEvalVisualizer(boxplot_folder)
        else:
            self.visualizer = None

        self.testbreaker_activated = testbreaker
        self.readonly = readonly
        self.keywordstats = keywordstats

        if not self.readonly:
            try:
                self.persistenceService.insert_test_execution(socket.gethostname())
            except:
                self.persistenceService.insert_test_execution("NO HOSTNAME")



    def start_suite(self, suite: TestSuite):
        """Geerbte Methode aus robot.api.ResultVisitor wird an dieser Stelle überschrieben, 
        um folgende Aktionen beim Aufruf jeder Testsuite durchzuführen:

        - Wegschreiben der Ausführungsergebnisse aller Tests der Testsuite
        - Performanzstatiskten abrufen und für HTML aufbereiten
        - weitere Daten für Boxplot holen und Boxplot genieren


        :param suite: übergebene TestSuite inkl. aller Tests
        :type suite: TestSuite (siehe robot.api)
        """
        if  not suite.suites:
            testcase_perf_stats = self.persistenceService.select_testcase_stats_filtered_by_suitename(suite.longname)

            joined_test_results: List[JoinedPerfTestResult] = self._eval_perf_of_tests(suite.tests, testcase_perf_stats)
            text: str = self._get_perf_result_table(joined_test_results)
            
            self.perf_results_list_of_testsuite = joined_test_results

            if self.boxplot_activated:
                testruns = self.persistenceService.select_testcase_runs_filtered_by_suitename(suite.longname)

                if len(testruns) == 0:
                    text+= "\n *Box-Plot* \n\n No historical data to generate the Boxplot"
                else:
                    rel_path_boxplot = self.visualizer.generate_boxplot_of_tests(testruns,suite.tests)
                    text+= "\n *Box-Plot* \n\n  ["+ rel_path_boxplot + "| Boxplot ]"


            suite.metadata["Performance Analysis"] = text

            if  not suite.suites and not self.readonly:
                self.persistenceService.insert_multiple_testcase_runs(suite.tests)


    def visit_test(self, test):
        """Geerbte Methode aus robot.api.ResultVisitor wird an dieser Stelle überschrieben, 
        um im Testbreaker-Modus die Testfälle bei schlechter Performanz auf FAIL zu setzen.
        Zudem wird über alle Keywords traversiert und ihre Laufzeiten gebündelt archiviert.

        :param test: übergebener Testfall
        :type test: TestCase (siehe robot.api)
        """
        if self.testbreaker_activated:
            for perf_result in self.perf_results_list_of_testsuite:
                if perf_result.longname == test.longname:
                    calced_devn = perf_result.devn
                    break
            if calced_devn:
                if calced_devn >self.max_deviation*100:
                    old_test_status = test.status
                    test.status = 'FAIL'
                    test.message = "PerfError: Test run lasted " + f'{calced_devn:.2f}' + " % than the average runs in the past and is thus above the maximum threshold of " + f'{self.max_deviation*100:.2f}' + " % (original test status was "+ str(old_test_status) + ")."

        if not self.readonly and self.keywordstats:
            self.body_items_of_test= []
            counter = 0
            if test.setup:
                counter = self._recursive_keywords_traversal(test.setup,test.longname,0, counter)

            for bodyItem in test.body:
                if isinstance(bodyItem,Keyword):
                    counter = self._recursive_keywords_traversal(bodyItem,test.longname,0, counter)
            if test.teardown:
                counter = self._recursive_keywords_traversal(test.teardown,test.longname,0, counter)

  
            self.persistenceService.insert_multiple_keyword_runs(self.body_items_of_test)

      
    def _recursive_keywords_traversal(self, bodyItem: Body, testcase_longname: str, level: int, counter: int):
        """Rekursiver Besuch aller Schlüsselwörter druch Pre-Order Traversal.
           Besuchte Schlüsselwörter werden in einer globalen Liste gechacht, bevor sie in die persistiert werden. 

        :param bodyItem: i. d. R. das eigentliche Schlüsselwort
        :type bodyItem: Body
        :param testcase_longname: Testfall im Rahmen dessen dieser Schlüsselwort aufgerufen wurde.
        :type testcase_longname: str
        :param level: Baumtiefe (dient später zur Unterscheidung zwischen High- und Low-Level-Keywords)
        :type level: int
        :param counter: Nummer des Elternkontens im Pre-Order
        :type counter: int
        :return: liefert die neue Nummer gemäß Pre-Order
        :rtype: int
        """

        if isinstance(bodyItem,Keyword):
            level+=1
            counter+=1
            if isinstance(bodyItem.parent, Keyword):
                parentname = bodyItem.parent.kwname
            else:
                parentname = "NO KEYWORD"

            self.body_items_of_test.append(Keywordrun(bodyItem.kwname,bodyItem.name,testcase_longname, parentname,bodyItem.libname,str(bodyItem.starttime),str(bodyItem.elapsedtime),bodyItem.status,level,counter))
            for children in bodyItem.body:
                counter = self._recursive_keywords_traversal(children,testcase_longname,level, counter)
        return counter


    def _eval_perf_of_tests(self, tests, perfstats) -> List[JoinedPerfTestResult]:
        """Interne Methode zum Zusammenbauen der Daten zur aktuellen Ausführung und zur Performanzstatistik.

        :param tests: Liste von Testfällen 
        :type tests: List[TestCase] (siehe Robot.result.model)
        :param perfstats: Liste von mehreren Testfällen und deren Statistikkennzahlen
        :type perfstats: List[TestPerfStats] (siehe model.py)
        :return: Liste der Testfälle mit Daten zur aktuellen Ausführung und Statistik
        :rtype: List[JoinedPerfTestResult] (siehe model.py)
        """

        #TODO: Eval-by=avg
        joined_stat_results = []
        for t in tests: 
            isInStats = False
            for ps in perfstats:
                if ps[1] == t.longname:
                    joined_test = JoinedPerfTestResult(name=t.name,longname=t.longname,elapsedtime=t.elapsedtime,avg=ps[2],min=ps[3],max=ps[4],count=ps[5],devn=((t.elapsedtime-ps[2])/ps[2])*100)
                    joined_stat_results.append(joined_test)
                    perfstats.remove(ps)
                    isInStats = True
                    break
            if not isInStats:
                joined_test = JoinedPerfTestResult(name=t.name,longname=t.longname,elapsedtime=t.elapsedtime,avg=None,min=None,max=None,count=None,devn=None)
                joined_stat_results.append(joined_test)
        return joined_stat_results


    def _get_perf_result_table(self, joined_perf_result_list: List[JoinedPerfTestResult]):
        """Interne Methode zum Erzeugen der formatierten Tabelle `Performance Analysis`.

        :param joined_perf_result_list: iste der Testfälle mit Daten zur aktuellen Ausführung und Statistik
        :type joined_perf_result_list: List[JoinedPerfTestResult]
        :return: formatierter Text bzw. Tabelle
        :rtype: str
        """
        text: str = TEXT_PERF_ANALYSIS_TABLE_HEADING
        for t in joined_perf_result_list:
            text+= TEXT_PERF_ANALYSIS_TABLE_ROW.format(name=t.name,elapsedtime=self._format_time_string(t.elapsedtime),avg=self._format_time_string(t.avg) if t.avg is not None else "NO STATS",min=self._format_time_string(t.min) if t.min is not None else "NO STATS",max=self._format_time_string(t.max) if t.max is not None else "NO STATS",count=t.count if t.count is not None else "NO STATS",devn=f'{t.devn:.2f}' if t.devn is not None else "NO STATS")
        return text

    def _format_time_string(self, val):
        return datetime.fromtimestamp(int(val) / 1e3).strftime("%M:%S.%f")[:-3]
