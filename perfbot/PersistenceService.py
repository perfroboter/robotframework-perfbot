from abc import abstractmethod, ABCMeta
from robot.result.model import TestCase
from model import *
from typing import List

class PersistenceService:
    """Abstrakte Klasse, um die eigentliche Implementierung, 
    wie die Testlaufergebnisse gespeichert bzw. abgerufen werden zu verschleiern.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert_testrun(self, test):
        """Speichern des Ergebnisses eines Testfalls. 

        :param test: zu speichernder TestCase
        :type test: TestCase (siehe robot.result.model)
        """
        pass

    @abstractmethod
    def insert_multiple_testruns(self, tests):
        """Speichern der Ergebnisse von mehreren Testfällen

        :param tests: zu speichernde TestFälle
        :type tests: Liste von TestCase(s) (siehe robot.result.model)
        """
        pass

    @abstractmethod
    def select_testruns_by_testname(self, test_name, limit) -> List[StoredTestrun]:
        """Liefert die Liste aller bisher gespeicherten Testergebnisse eines Testfalls, selektiert beim Testnamen.

        :param test_name: Name des Testfalls
        :type test_name: str
        :param limit: Möglichkeit nur die letzten x Testergebnisse zu selektieren
        :type limit: int
        :return: Liste von Testlaufergebnissen (siehe model.py)
        :rtype: List[Testrun]
        """
        pass

    @abstractmethod
    def select_multiple_testruns_by_suitename(self, suite_name) -> List[StoredTestrun]:
        """Liefert die Liste aller bisher gespeicherten Testergebnisse aller Tests einer TestSuite, selektiert beim Namen der Testsuite.

        :param suite_name: Name der Testsuite (longname)
        :type suite_name: str
        :return:Liste von Testlaufergebnissen (siehe model.py)
        :rtype: List[Testrun]
        """
        pass

    @abstractmethod
    def select_stats_grouped_by_suitename(self, suite_name) -> List[TestPerfStats]:
        """Liefert aggregierte Statistiken aller Testfälle einer TestSuite, gruppiert nach Testfallnamen.

        :param suite_name: Name der Testsuite (longname)
        :type suite_name: str
        :return: Liste der Performanzstatistik (siehe model.py)
        :rtype: List[TestPerfStats]
        """
        pass



