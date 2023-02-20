from abc import abstractmethod, ABCMeta
from robot.result.model import TestCase
from model import *
from typing import List

class PersistenceService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert_testrun(self, test):
        pass

    @abstractmethod
    def insert_multiple_testruns(self, tests):
        pass

    @abstractmethod
    def select_testruns_by_testname(self, test_name, limit) -> List[Testrun]:
        pass

    @abstractmethod
    def select_multiple_testruns_by_suitename(self, suite_name) -> List[Testrun]:
        pass

    @abstractmethod
    def select_stats_grouped_by_suitename(self, suite_name) -> List[TestPerfStats]:
        pass



