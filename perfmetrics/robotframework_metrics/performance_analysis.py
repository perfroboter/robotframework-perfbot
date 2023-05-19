from perfbot.PersistenceService import PersistenceService
from perfbot.PerfEvalVisualizer import PerfEvalVisualizer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os, glob
from pathlib import Path
import io
import logging
import seaborn as sns

class PerformanceAnalysis():

    def __init__(self, suite_list, test_list, kw_list, persistenceService, perf_analysis):
        self.suite_list = suite_list
        self.test_list = test_list
        self.kw_list = kw_list
        self.persistenceService: PersistenceService = persistenceService
        self.perfEvalVisualizer: PerfEvalVisualizer = PerfEvalVisualizer(None)
        self.perf_analysis = perf_analysis

    def generate_boxplot_of_positional_keyword(self, keyword_json):
        hist_data = self.persistenceService.select_keyword_runs_filtered_by_positional_keyword(keyword_json["TestName"], keyword_json["Name"], keyword_json["Stepcounter"])
        hist = pd.DataFrame(hist_data, columns =["testcase_name" , "testcase_longname" , "suitename" , "kw_name" , "kw_longname" , "libname" , "starttime" , "elapsedtime" , "status" , "keyword_level" , "stepcounter" , "parent_keyword_longname" , "id" , "hostname"])
        temp = []
        temp.append(keyword_json)
        
        act = pd.DataFrame(temp,columns =["Name", "TestName", "Libname","Libname", "Time", "Stepcounter"], copy=True)
        act["elapsedtime"] = act["Time"]
        act["kw_longname"] = act["Name"]
        return self.perfEvalVisualizer.generate_boxplot(hist,act,y="kw_longname",ylabel="Keyword",heading="Box-Plot of keyword duration times")

    def generate_boxplot_of_one_test(self, hist_tests, act_test):
        hist = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        temp = []
        temp.append(act_test)
        act = pd.DataFrame(temp,columns =["Test Name" , "Test Longname",  "Status (Act)","Time (Act)", "Starttime"], copy=True)
        act["elapsedtime"] = act["Time (Act)"]
        act["name"] = act["Test Name"]
        
        return self.perfEvalVisualizer.generate_boxplot(hist, act, format="svg")

    def generate_boxplot_of_tests(self, hist_tests, act_tests):
        hist = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        act = pd.DataFrame(act_tests, copy=True)
        act["elapsedtime"] = act["Time (Act)"]
        act["name"] = act["Test Name"]
        return self.perfEvalVisualizer.generate_boxplot(hist, act, format="svg")

    #def generate_boxplot(self, hist_results: pd.DataFrame, act_results: pd.DataFrame, x="elapsedtime", y='name', xlabel="Duration (s)",ylabel="Testcase", heading='Box-Plot of the test duration times', format="svg"):

    def generate_timeline_of_multiple_tests(self,hist_tests, act_tests):
        sns.set_theme(style="whitegrid", context="notebook")
        df = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        df["elapsedtime"] = df["elapsedtime"].astype(int) / 1000
        df['starttime'] = pd.to_datetime(df['starttime'], format='%Y%m%d %H:%M:%S.%f')
        df['ts'] =  df['starttime'].astype(int) 

        
        #df.set_index('ts', inplace=True)
        #Format startime as date
        timeline = sns.scatterplot(data=df,x="starttime",y="elapsedtime", hue="name",markers=True)
        
       # timeline.set(xticklabels=[])  # remove the tick labels
       # timeline.tick_params(bottom=False)  # remove the ticks
        timeline.legend_.set_title(None)

        if act_tests:
            act = pd.DataFrame(act_tests, copy=True)
            act["Starttime"] = pd.to_datetime(act["Starttime"], format='%Y%m%d %H:%M:%S.%f')
            act['ts'] =  act["Starttime"].astype(int)
            act["elapsedtime"] = act["Time (Act)"].astype(int) / 1000
            act["name"] = act["Test Name"]
            stipplot = timeline.plot(act["Starttime"], act["elapsedtime"],'o', color='black')
        
        #timeline.set_xticklabels(timeline.get_xticklabels(), rotation=45, horizontalalignment='right')
        timeline.xaxis.set_major_formatter(mdates.ConciseDateFormatter(timeline.xaxis.get_major_locator()))
        f = io.StringIO()
        timeline.figure.savefig(f, format = "svg",  bbox_inches="tight")
        plt.clf()
        return f.getvalue()

    @staticmethod
    def getTestsPerfStats(perf_analysis):
        test_perf_list = []
        for suite in perf_analysis:
             for test in suite["Tests"]:
                        perf_test_stats = {
                        "Test Name" :test["Test Name"],
                        "Test Longname" :test["Test Longname"],
                        "Status (Act)": test["Status (Act)"],
                        "Time (Act)": int(test["Time (Act)"]),
                        "Avg": int(test["Avg"]),
                        "P75": int(test["P75"]),
                        "P25": int(test["P25"]),
                        "DevnAvg": (int(test["Time (Act)"]) - int(test["Avg"]))/int(test["Avg"]),
                        "Devn75": (int(test["Time (Act)"]) - int(test["P75"]))/int(test["P75"]),
                        "Devn25": (int(test["Time (Act)"]) - int(test["P25"]))/int(test["P25"]),
                        }
                        test_perf_list.append(perf_test_stats)
        return test_perf_list


    def analysePerformance(self):
        suite_perf_list = []
        # Bottom-Up
        # Erst über Keywords iterieren und Statistiken und SVG-Grafiken speichern
        # Ergebnisse zwischenspeichern
        # Über Testfälle iterieren und Statisitken und SVG-Grafiken speichern (Ergebnisse der Keyword-Ebene können genutzt werden)
        for suite in self.suite_list:
            suite_perf_json = {
                 "Suite Name": suite["Name"],
                 "Status (Act)": suite["Status"],
                "Time (Act)": suite["Time"],
                "Tests": [],
                "Boxplot": None,
                "Timeline": None,
                "Difference": None
            }
            suite_perf_list.append(suite_perf_json)

        for test in self.test_list:
            perf_stats = self.persistenceService.select_testcase_stats_filtered_by_testname(str(test["Test Longname"]))

            if len(perf_stats)==0:
                avg="NO STATS"
                min="NO STATS"
                max="NO STATS"
                count="0"
            else:
                avg=int(perf_stats[0][2])
                min=int(perf_stats[0][3])
                max=int(perf_stats[0][4])
                count=int(perf_stats[0][5])

            test_perf_json = {
                "Test Name": test["Test Name"],
                "Test Longname": test["Test Longname"],
                "Status (Act)": test["Status"],
                "Time (Act)": test["Time"],
                "Starttime": test["Starttime"],
                "Avg": avg,
                "Min": min,
                "Max": max,
                "Count": count,
                "Boxplot": None,
                "Timeline": None,
                "Std": None,
                "P25": None,
                "P50": None,
                "P75": None,
                "Keywords": []
            }

            
            perf_keyword_stats = self.persistenceService.select_positional_keyword_stats(test["Test Longname"])
            for keyword in self.kw_list:
                for perf_keyword in perf_keyword_stats:
                    #"SELECT kw_name 0, kw_longname 1, testcase_longname 2, parent_keyword_longname 3, libname 4, keyword_level 5, stepcounter 6, avg(elapsedtime) as avg 7, min(elapsedtime) as min, max(elapsedtime) as max, count(elapsedtime) as count FROM keyword_run_view GROUP BY testcase_longname, kw_longname, stepcounter;"
                    #TODO: Auf Status im Select filtern
                    #TODO: Hinweis auf keine Stats, wenn keine gefunden
                    if perf_keyword[2] == keyword["TestName"] and perf_keyword[1] == keyword["Name"] and perf_keyword[6] == keyword["Stepcounter"]:
                
                        keyword_perf_json = {
                        "Name" : keyword["Name"],
                        "TestName": keyword["TestName"],
                        "Libname": keyword["Libname"],
                        "Status" : keyword["Status"],
                        "Time" : keyword["Time"],
                        "Stepcounter": keyword["Stepcounter"],
                        "Level": int(perf_keyword[5]),
                        "Avg": int(perf_keyword[7]),
                        "Min": int(perf_keyword[8]),
                        "Max": int(perf_keyword[9]),
                        "Count": int(perf_keyword[10]),
                        "Boxplot": None,
                        "Std": None,
                        "P25": None,
                        "P50": None,
                        "P75": None,
                        }
                        keyword_perf_json["Boxplot"] = self.generate_boxplot_of_positional_keyword(keyword_perf_json)
                        hist_data = self.persistenceService.select_keyword_runs_filtered_by_positional_keyword(keyword_perf_json["TestName"], keyword_perf_json["Name"], keyword_perf_json["Stepcounter"])
                        k_stats = pd.DataFrame(hist_data, columns =["testcase_name" , "testcase_longname" , "suitename" , "kw_name" , "kw_longname" , "libname" , "starttime" , "elapsedtime" , "status" , "keyword_level" , "stepcounter" , "parent_keyword_longname" , "id" , "hostname"])['elapsedtime'].astype(int).describe()
                        keyword_perf_json["Std"] = k_stats["std"]
                        keyword_perf_json["P25"] = k_stats["25%"]
                        keyword_perf_json["P50"] = k_stats["50%"]
                        keyword_perf_json["P75"] = k_stats["75%"]

                        test_perf_json["Keywords"].append(keyword_perf_json)
            
            testcase_runs = self.persistenceService.select_testcase_runs_filtered_by_testname(test["Test Longname"])
            t_stats = pd.DataFrame(testcase_runs, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"])['elapsedtime'].astype(int).describe()
            test_perf_json["Std"] = t_stats["std"]
            test_perf_json["P25"] = t_stats["25%"]
            test_perf_json["P50"] = t_stats["50%"]
            test_perf_json["P75"] = t_stats["75%"]
            test_perf_json["Boxplot"] = self.generate_boxplot_of_one_test(testcase_runs,test_perf_json)
            test_perf_json["Timeline"] = self.generate_timeline_of_multiple_tests(testcase_runs,None)
            for perf_suite in suite_perf_list:
                if(perf_suite["Suite Name"] == str(test["Suite Longname"])):
                    perf_suite["Tests"].append(test_perf_json)
                    break

        for perf_suite in suite_perf_list:
            hist_testcases = self.persistenceService.select_testcase_runs_filtered_by_suitename(perf_suite["Suite Name"])
            act_testcases = perf_suite["Tests"]
            perf_suite["Boxplot"] = self.generate_boxplot_of_tests(hist_testcases,act_testcases)
            perf_suite["Timeline"] = self.generate_timeline_of_multiple_tests(hist_testcases,act_testcases)
            
        self.perf_analysis = suite_perf_list

        return self.perf_analysis