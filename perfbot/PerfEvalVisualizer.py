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

    def __init__(self, boxplot_folder=None):
        self.boxplot_folder = boxplot_folder

    def generate_boxplot_of_tests(self, hist_tests, act_tests):
        """Wrapper zum Aufruf von :py:meth:`~PerfEvalVisualizer.generate_boxplot()`.
        :param hist_tests: historische Daten als Liste
        :type hist_tests: list
        :param act_tests: aktuelle Daten als list
        :type act_tests: list
        :return: Pfad zur Bilddatei
        :rtype: str
        """
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
        """Generische Generation des Boxplots aus pd.DataFrames.
           Kontrekt wird ein Box-Plot erzeugt, darauf eine Punktwolke aller Werte und durch einen orangen Punkt die aktuelle Laufzeit.

        :param hist_results: Historische Daten aus denen der Boxplot generiert wird
        :type hist_results: pd.DataFrame
        :param act_results: Aktuelle Daten, die aktuelle Laufzeit im Boxplot makieren
        :type act_results: pd.DataFrame
        :param x: Spaltenname der x-Achse in den DataFrames, defaults to "elapsedtime"
        :type x: str, optional
        :param y: Spaltenname der y-Achse in den DataFrames, defaults to 'name'
        :type y: str, optional
        :param xlabel: Beschriftung der x-Achse, defaults to "Duration (s)"
        :type xlabel: str, optional
        :param ylabel: Beschriftung der y-Achse, defaults to "Testcase"
        :type ylabel: str, optional
        :param heading: Titel, defaults to 'Box-Plot of the test duration times'
        :type heading: str, optional
        :param format: Dateformat, ob ein Pfad zur Bilddatei oder ein SVG als String zurückgegeben wird, defaults to "svg"
        :type format: str, optional
        :return: Pfad zur Bilddatei oder SVG-String
        :rtype: str
        """
        sns.set_theme(style="whitegrid", context="notebook")
        hist = pd.DataFrame(hist_results, copy=True)
        hist[x] = hist[x].astype(int) / 1000
        boxplot = sns.boxplot(x=x, y=y, data=hist)

        boxplot.set_xlabel(xlabel)
        boxplot.set_ylabel(ylabel)
        boxplot.figure.suptitle(heading, fontsize=14, fontweight='bold')
        boxplot.set_title("")
        
        sns.stripplot(ax=boxplot,x=x, y=y, data=hist, color="grey")

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
