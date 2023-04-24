import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os, glob
from pathlib import Path

class PerfEvalVisualizer:
    """Diese Klasse übernimmt die visuelle Aufbereitung von Performanzdaten der Testfälle.

    :return: _description_
    :rtype: _type_
    """

    def __init__(self, boxplot_folder):
        self.boxplot_folder = boxplot_folder

    def generate_boxplot_of_suite(self, hist_tests, act_tests):
        """generiert ein Boxplot bzw. ein Bild mit ggf. mehren Boxplots. 
        Pro Testfall wird ein Boxplot gezeichnet und darin die aktuelle Testlaufzeit dargestellt.


        :param hist_tests: Liste der historischen Testläufe der Testfälle
        :type hist_tests: List[Testrun] (siehe model.py)
        :param act_tests: Liste der aktuellen Testfälle
        :type act_tests: 
        :return: Pfad zur Bilddatei
        :rtype: str
        """
        df = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"])
        df["elapsedtime"] = df["elapsedtime"].astype(int)
        boxplot = df.boxplot(column=['elapsedtime'], by=['name'], fontsize=8, vert=False)

        boxplot.set_xlabel("Elapsed time in ms")
        boxplot.set_ylabel("Testcases")
        boxplot.figure.suptitle('Box-Plot of the test duration times', fontsize=14, fontweight='bold')
        boxplot.set_title("")
        
        i = 1
        for label in boxplot.get_yticklabels():
            for t in act_tests:
                if t.name == label.get_text():
                    boxplot.plot(t.elapsedtime,i,marker="o")
            i=i+1
        time = datetime.now()

        Path(self.boxplot_folder).mkdir(parents=True, exist_ok=True)
        pathname  = self.boxplot_folder + "boxplot" + time.strftime("-%m-%d-%Y-%H-%M-%S-%f") + ".png"
        try:
            plt.savefig(pathname, bbox_inches="tight")
        except:
            print("An execption occured")
        return pathname
        
