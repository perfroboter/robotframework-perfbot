import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io
from pathlib import Path
import seaborn as sns

class PerfEvalVisualizer:
    """Diese Klasse übernimmt die visuelle Aufbereitung von Performanzdaten der Testfälle.

    :return: _description_
    :rtype: _type_
    """

    def __init__(self, boxplot_folder):
        self.boxplot_folder = boxplot_folder

    def generate_boxplot_of_tests(self, hist_tests, act_tests):
        hist = pd.DataFrame(hist_tests, columns =["id" ,"name", "longname", "starttime" , "elapsedtime" , "status"], copy=True)

        t_list = []
        for t in act_tests:
            t_json = {
                "name": t.name,
                "longname": t.longname,
                "elapsedtime": t.elapsedtime
            }
            t_list.append(t_json)
        act = pd.DataFrame(t_list, columns =["name", "longname", "elapsedtime"], copy=True)

        return self.generate_boxplot(hist, act, format="png")

    def generate_boxplot(self, hist_results: pd.DataFrame, act_results: pd.DataFrame, x="elapsedtime", y='name', xlabel="Duration (s)",ylabel="Testcase", heading='Box-Plot of the test duration times', format="svg"):
        sns.set_theme(style="whitegrid", context="notebook")
        hist = pd.DataFrame(hist_results, copy=True)
        hist[x] = hist[x].astype(int) / 1000
        boxplot = sns.boxplot(x=x, y=y, data=hist)

        boxplot.set_xlabel(xlabel)
        boxplot.set_ylabel(ylabel)
        boxplot.figure.suptitle(heading, fontsize=14, fontweight='bold')
        boxplot.set_title("")
        
        sns.stripplot(ax=boxplot,x=x, y=y, data=hist, color="grey")

        # Die Makierung der aktuellen Laufzeiten funktioniert nicht bzw. irgendwie werden die Figures dann doppelt referenziert...
        # Fehler gefunden: Timestamp %f wird nicht ausgefüllt
        if True:
            act = pd.DataFrame(act_results, copy=True)
            act[x] = act[x].astype(int) / 1000
            plt.plot(act[x], act[y],'o', color='orange', zorder=10)
        
        match format:
            case "svg":
                f = io.StringIO()
                boxplot.figure.savefig(f, format = "svg", bbox_inches="tight")
                plt.clf()
                return f.getvalue() 

            case "png":
                Path(self.boxplot_folder).mkdir(parents=True, exist_ok=True)
                pathname  = self.boxplot_folder + "boxplot" + datetime.now().strftime("-%m-%d-%Y-%H-%M-%S-%f") + ".png"
                try:
                    plt.savefig(pathname, bbox_inches="tight")
                    plt.clf()
                except:
                    print("An execption occured")
                print("Boxplot generiert: " + pathname)
                return pathname
            case _:
                raise KeyError("Wrong Format of Boxplot generation.")   
