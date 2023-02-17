import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os, glob

class PerfEvalVisualizer:
    hasDeleted = False

    def __init__(self):
        pass

    def generate_boxplot_of_suite(self, hist_tests, act_tests):
        df = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedTime" , "status"])
        df["elapsedTime"] = df["elapsedTime"].astype(int)
        boxplot = df.boxplot(column=['elapsedTime'], by=['name'], fontsize=8, vert=False)

        boxplot.set_xlabel("Elapsed time in ms")
        boxplot.set_ylabel("Testcases")
        boxplot.figure.suptitle('Box-Plot of the test duration times', fontsize=14, fontweight='bold')
        boxplot.set_title("")
        
        i = 1
        for label in boxplot.get_yticklabels():
            #label.get_text()
            for t in act_tests:
                if t.name == label.get_text():
                    boxplot.plot(t.elapsedtime,i,marker="o")
            i=i+1
        time = datetime.now()
        #TODO: Datei erzeugen und löschen ändern
        if not PerfEvalVisualizer.hasDeleted:
            for f in glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/" + "boxplot*.png"):
                os.remove(f)
            PerfEvalVisualizer.hasDeleted = True

        pathname  = os.path.dirname(os.path.abspath(__file__)) + "/" + "boxplot" + time.strftime("-%m-%d-%Y-%H-%M-%S-%f") + ".png"
        plt.savefig(pathname, bbox_inches="tight")
        return pathname
        