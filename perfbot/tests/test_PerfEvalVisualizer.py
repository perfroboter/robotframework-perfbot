import unittest
from ..PerfEvalVisualizer import *
import os


class TestSqlite3PersistenceService(unittest.TestCase):
    NAME_OF_TEST_BOXPLOT_FOLDER = "temp"

    def setUp(self):
        self.evalVisualizer = PerfEvalVisualizer(os.path.dirname(__file__) + "/" + self.NAME_OF_TEST_BOXPLOT_FOLDER)
        self.hist_tests = [(1," Invalid Username", "Tests.Invalid Login.Invalid Username", "20230427 09:57:55.116",666,"PASS"),
                      (2," Invalid Username", "Tests.Invalid Login.Invalid Username", "20230427 09:58:14.637",400,"PASS"),
                      (1," Invalid Username", "Tests.Invalid Login.Invalid Username", "20230427 09:57:58.631",3593,"PASS"),
                      (2," Valid Login", "Tests.Valid Login.Valid Login", "20230427 09:57:55.116",3361,"PASS")]
        self.act_tests = [(1," Invalid Username", "Tests.Invalid Login.Invalid Username", "20230427 09:59:02.255",398,"PASS"),
                    (2," Valid Login", "Tests.Valid Login.Valid Login", "20230427 09:59:04.598",3730,"PASS")]

    def tearDown(self):
      #  folder = os.path.dirname(__file__) + "/" + self.NAME_OF_TEST_BOXPLOT_FOLDER
      #  Remove folder
        pass

    def test_boxplot(self):
        hist = pd.DataFrame(self.hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        act = pd.DataFrame(self.act_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)

        svg_string: str = self.evalVisualizer.generate_boxplot(hist_results=hist,act_results=act)
        self.assertTrue("</svg>" in svg_string)