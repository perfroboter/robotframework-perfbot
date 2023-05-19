from robot.api import ResultVisitor
from robot.result.model import Keyword, TestCase

class KeywordResults(ResultVisitor):

    def __init__(self, kw_list, ignore_library, ignore_type):
        self.kw_list = kw_list
        self.ignore_library = ignore_library
        self.act_testcase_longname = None
        #self.ignore_type = ignore_type
        self.stepcounter = 0
    
    def start_test(self, test):
        self.act_testcase_longname = test.longname
        self.stepcounter = 0

    def start_keyword(self, kw: Keyword):
        if self.act_testcase_longname: # Suite-Setup-Keywords etc. werden damit rausgefiltert
            self.stepcounter+=1
            kw_json = {
                "Name" : kw.name,
                "TestName": self.act_testcase_longname,
                "Libname": kw.libname,
                "Status" : kw.status,
                "Time" : kw.elapsedtime,
                "Parent": kw.parent,
                "Stepcounter": self.stepcounter
            }
            self.kw_list.append(kw_json)