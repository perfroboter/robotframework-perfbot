from .PersistenceService import PersistenceService
import pandas as pd
import matplotlib.pyplot as plt
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
        self.perf_analysis = perf_analysis

    def generate_boxplot_of_multiple_tests(self, hist_tests, act_tests):
        sns.set_theme(style="darkgrid")
        df = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        df["elapsedtime"] = df["elapsedtime"].astype(int) / 1000
        boxplot = sns.boxplot(x='elapsedtime', y='name', data=df)

        boxplot.set_xlabel("Elapsed time in ms")
        boxplot.set_ylabel("Testcases")
        boxplot.figure.suptitle('Box-Plot of the test duration times', fontsize=14, fontweight='bold')
        boxplot.set_title("")
        
        sns.stripplot(ax=boxplot,x="elapsedtime", y="name", data=df, color="grey")

        if act_tests:
            act = pd.DataFrame(act_tests, copy=True)
            act["elapsedtime"] = act["Time (Act)"].astype(int) / 1000
            act["name"] = act["Test Name"]
            sns.stripplot(ax=boxplot,x="elapsedtime", y="name", data=act, size=7, jitter=False,color="black")
        
        
        
        
        f = io.StringIO()
        boxplot.figure.savefig(f, format = "svg",  bbox_inches="tight")
        plt.clf()
        return f.getvalue() 

    def generate_timeline_of_multiple_tests(self,hist_tests, act_tests):
        sns.set_theme(style="darkgrid")
        df = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)
        df["elapsedtime"] = df["elapsedtime"].astype(int) / 1000
        df['starttime'] = pd.to_datetime(df['starttime'], format='%Y%m%d %H:%M:%S.%f')
        df['ts'] =  df['starttime'].astype(int) 

        
        #df.set_index('ts', inplace=True)
        #Format startime as date
        timeline = sns.lineplot(data=df,x="ts", y="elapsedtime",hue="name",markers=True)
        
        timeline.set(xticklabels=[])  # remove the tick labels
        timeline.tick_params(bottom=False)  # remove the ticks
        timeline.legend_.set_title(None)

        if act_tests:
            act = pd.DataFrame(act_tests, copy=True)
            act["Starttime"] = pd.to_datetime(act["Starttime"], format='%Y%m%d %H:%M:%S.%f')
            act['ts'] =  act["Starttime"].astype(int)
            act["elapsedtime"] = act["Time (Act)"].astype(int) / 1000
            act["name"] = act["Test Name"]
            stipplot = timeline.plot(act["ts"], act["elapsedtime"],'o', color='black')
        
        f = io.StringIO()
        timeline.figure.savefig(f, format = "svg",  bbox_inches="tight")
        plt.clf()
        return f.getvalue()

    def generate_barplot_difference(self, names, act, hist):
        sns.set_theme(style="white", context="talk")
        rs = np.random.RandomState(8)

        # Set up the matplotlib figure
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 5), sharex=True)

        # Generate some sequential data
        x = np.array(list("ABCDEFGHIJ"))
        y1 = np.arange(1, 11)
        sns.barplot(x=names, y=act, palette="rocket", ax=ax1)
        ax1.axhline(0, color="k", clip_on=False)
        ax1.set_ylabel("ACTUAL")

        # Center the data to make it diverging
        y2 = act - hist
        sns.barplot(x=x, y=y2, palette="vlag", ax=ax2)
        ax2.axhline(0, color="k", clip_on=False)
        ax2.set_ylabel("Difference")

        # Randomly reorder the data to make it qualitative
        sns.barplot(x=x, y=hist, palette="deep", ax=ax3)
        ax3.axhline(0, color="k", clip_on=False)
        ax3.set_ylabel("HIST")

        # Finalize the plot
        sns.despine(bottom=True)
        plt.setp(f.axes, yticks=[])
        plt.tight_layout(h_pad=2)
        f = io.StringIO()
        plt.savefig(f, format = "svg")
        plt.clf()
        return f.getvalue()


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
                        "Count": int(perf_keyword[10])
                        }
                        test_perf_json["Keywords"].append(keyword_perf_json)

            test_perf_json["Boxplot"] = self.generate_boxplot_of_multiple_tests(self.persistenceService.select_testcase_runs_filtered_by_testname(test["Test Longname"]),None)
            for perf_suite in suite_perf_list:
                if(perf_suite["Suite Name"] == str(test["Suite Longname"])):
                    perf_suite["Tests"].append(test_perf_json)
                    break

        for perf_suite in suite_perf_list:
            hist_testcases = self.persistenceService.select_testcase_runs_filtered_by_suitename(perf_suite["Suite Name"])
            act_testcases = perf_suite["Tests"]
            perf_suite["Boxplot"] = self.generate_boxplot_of_multiple_tests(hist_testcases,act_testcases)
            perf_suite["Timeline"] = self.generate_timeline_of_multiple_tests(hist_testcases,None)
            
        self.perf_analysis = suite_perf_list

        return self.perf_analysis