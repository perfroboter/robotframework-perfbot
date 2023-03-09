from PerfEvalResultModifier import PerfEvalResultModifier

"""Hier ist der Einstiegspunkt von perfbot: 

Perfbot ermittelt Performance-Veränderungen anhand von bestehenden 
automatisierten UI-Tests. Es erweitert dabei das 
[Robot Framework](http://www.robotframework.org) 
um die Möglichkeit, Test-Laufzeiten in einer Datenbank zu 
speichern und mit den archivierten Laufzeiten der Vergangenheit zu vergleichen. 
Das Ergebnisse der Performance-Analyse werden in die Robot-Testresults 
(`log.html` / `report.html`) integriert.
"""

class perfbot(PerfEvalResultModifier):
    """Dies ist nur ein Wrapper, damit der Aufruf mit dem Parameter --prerebotmodifier perfbot/perfbot.py aufgerufen werden kann.
    
    :param PerfEvalResultModifier: Basisklasse in der die eigentliche Logik stattfindet. 
    """
    pass