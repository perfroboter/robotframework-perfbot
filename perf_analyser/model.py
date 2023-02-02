from typing import NamedTuple
from robot.result.model import TestCase


class JoinedPerfTestResult(NamedTuple):
        name: str
        longname: str
        elapsedtime: any
        avg: any
        min: any
        max: any
        count: any
        devn: any

class Testrun:
    name = None
    longname = None
    starttime = None
    elapsedtime = None
    status = None

    def __init__(self, name: str, longname:str , starttime: str, elapsedtime: int, status: str):
        #name, longname, starttime, elapsedTime, status
        self.name = name
        self.longname = longname
        self.starttime = starttime
        self.elapsedtime = elapsedtime
        self.status = status

    @staticmethod
    def from_robot_testCase(test: TestCase):
        return Testrun(test.name, test.longname, str(test.starttime), test.elapsedtime, test.status)

    def get_values_as_tuple(self):
        return tuple(self.__dict__.values())

class TestPerfStats:
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