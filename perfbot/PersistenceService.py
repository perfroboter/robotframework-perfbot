from abc import abstractmethod, ABCMeta
from robot.result.model import TestCase
from .model import *
from typing import List

class PersistenceService:
    """Abstrakte Klasse, um die eigentliche Implementierung, 
    wie die Testlaufergebnisse gespeichert bzw. abgerufen werden zu verschleiern.
    """
    __metaclass__ = ABCMeta
    #TODO: Doku wiederherstellen

    @abstractmethod
    def insert_test_execution(self, host_name):
        pass

    @abstractmethod
    def insert_testcase_run(self, testrun):
        pass
    
    @abstractmethod
    def insert_multiple_testcase_runs(self, testruns):
        pass

    @abstractmethod
    def insert_keyword_run(self, keywordrun):
        pass
    
    @abstractmethod
    def insert_multiple_keyword_runs(self, keywordruns):
        pass

    @abstractmethod
    def select_testcase_runs_filtered_by_testname(self, testcase_longname):
        pass

    @abstractmethod
    def select_testcase_runs_filtered_by_suitename(self, suite_longname):
        pass
    
    @abstractmethod
    def select_testcase_stats_filtered_by_testname(self, testcase_longname):
        pass

    @abstractmethod
    def select_testcase_stats_filtered_by_suitename(self, suite_longname):
        pass

    @abstractmethod
    def select_keyword_runs_filtered_by_testname(self, testcase_longname):
        pass

    @abstractmethod
    def select_keyword_runs_filtered_by_suitename(self, suite_longname):
        pass
    
    @abstractmethod
    def select_global_keyword_stats(self):
        pass

    @abstractmethod
    def select_positional_keyword_stats(self, testcase_filter=None):
        pass