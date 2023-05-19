from robot.api import ResultVisitor
from robot.utils.markuputils import html_format
from .PersistenceService import PersistenceService


class TestResults(ResultVisitor):

    def __init__(self, test_list):
        self.test_list = test_list
    
    def visit_test(self, test):
        
        test_json = {
            "Suite Name" : test.parent,
            "Suite Longname": test.parent.longname,
            "Test Name" : test.name,
            "Test Longname": test.longname,
            "Test Id" : test.id,
            "Status" : test.status,
            "Documentation" : html_format(test.doc),
            "Time" : test.elapsedtime,
            "Starttime": test.starttime,
            "Message" : html_format(test.message),
            "Tags" : test.tags
        }
        self.test_list.append(test_json)