from typing import NamedTuple
from robot.result.model import TestCase

"""Zentrale Datei für das Datenmodell von perfbot.

Dieses Datenmodell ergänzt nur das vorhandene Datenmodell robot.model bzw. robot.result.model 
an notwendigen Stellen. Ansonsten wird das Datenmodell von robot genutzt.
"""

class JoinedPerfTestResult(NamedTuple):
    """Vereint die relevanten Daten des TestCase aus den Robot-Datenmodell und 
    den Statistiken zu diesem Testfall, die durch perfbot ermittelt wurden.

    :param NamedTuple: Basisklasse
    """
    name: str
    longname: str
    elapsedtime: any
    avg: any
    min: any
    max: any
    count: any
    devn: any

class Testrun(NamedTuple):
    """Stellt die Repräsentation eines Testlaufs eines Testfalls dar. 
       (So wie es der PersistenceService zurück gibt.)
    """
    name: any
    longname: any
    starttime: any
    elapsedtime: any
    status: any

    #def __init__(self, name: str, longname:str , starttime: str, elapsedtime: int, status: str):
    #    #name, longname, starttime, elapsedTime, status
    #    self.name = name
    #    self.longname = longname
    #    self.starttime = starttime
    #    self.elapsedtime = elapsedtime
    #    self.status = status

    @staticmethod
    def from_robot_testCase(test: TestCase):
        """Möglichkeit der Erzeugung basierend auf dem Robot-Datenmodell

        :param test: TestCase (siehe robot.result.model)
        :type test: TestCase
        :return: erzeugtes Objekt vom Typ Testrun
        :rtype: Testrun
        """
        return Testrun(test.name, test.longname, str(test.starttime), test.elapsedtime, test.status)

    def get_values_as_tuple(self):
        return tuple(self.__dict__.values())

    
class StoredTestrun(Testrun):
    id: any

    


class TestPerfStats:
    """Stellt Statistikkennzahlen eines Testfalls dar. Die Kennzahlen fassen i. d. R. mehrere Tetläufe des Testfalls zusammen.
        Die Testdaten 
       (So wie es der PersistenceService zurück gibt.)
    """
    name = None
    longname = None
    avg = None
    min = None
    max = None
    count = None

    def __init__(self, name, longname, avg, min, max, count):
        self.name = name
        self.longname = longname
        self.avg = avg
        self.min = min
        self.max = max
        self.count = count