# RobotPerfAnalyser: Robot-Testfälle als Indikator für Performance-Probleme nutzen

## Idee

Mittels des RobotResultModifier-Schnittstelle wird (nach der eigentlichen Testausführung vor Erstellung der Reports) die aktuelle Testdauer jedes Testfalls analyisiert und mit einem Maximalwert und dem Durchschnitt der letzten Läufe der Vergangenheit verglichen. Lässt sich daraus ein Performanzproblem erkennen, so wir der Testfall auf FAIL gesetzt und mit einer Message ausgestattet. Zu jeder Testsuite werden ausführliche Details zum Performanz-Vergleich ausgegeben.

## Architektur / Inhalt

- `perf_analyser/PerfEvalResultModifier.py`: Robot-Result-Modifier, der nach der Ausführung der Test die Performanz analysiert und die Ergebnisse in der log.html und report.html festhält
- `perf_analyser/PersistenceService.py` bzw. `perf_analyser/Sqlite3PersistenceService.py`: Zugriff und Persistierung der Testläufe (mittels Sqlite3-Datenbank)
- `perf_analyser/PerfEvalVisualizer.py`
- `sut`: Im Beispiel genutztes System-under-Test
- `testcases`: Beispiel-Testfälle
- `robot-exec-times.db`: Sqlite-Datenbank mit ersten historisierten Daten

## Quick Start
```bash
# Starten des System-under-Test (entnommen aus https://github.com/robotframework/SeleniumLibrary)
python3 sut/server.py

# Ausführung der beispielhaften Tests ohne PerfEval
# Vorher: Installationsanleitung gemäß https://github.com/robotframework/SeleniumLibrary
python3 -m robot testcases

# Ausführung der Tests mit PerfEval als ResultModifier
# Erläuterung: Der ResultModifier läuft nach der Ausführung aller Tests und verändert nur die log.html und report.html (output.xml und Kommandozeilenausgabe bleiben unverändert)
python3 -m robot --prerebotmodifier perf_analyser/PerfEvalResultModifier.py testcases


# Ausführung im Testbreaker-Modus
# Erläuterung: Bei einer Abweichung der Testlaufzeit von über 10% (0.1) vom Durchschnitt der vergangen Testläufe wir der Testfall auf "FAIL" gesetzt
python3 -m robot --prerebotmodifier perf_analyser/PerfEvalResultModifier.py:devn=0.1:db_path="robot-exec-times.db"testbreaker=True testcases

# Ausführung im Boxplot-Modus
# Erläuterung: Die Testlaufzeiten aller Testfälle einer Suite werden als Boxplot dargestellt (Voraussetzung: pandas und matplotlib)
python3 -m robot --prerebotmodifier perf_analyser/PerfEvalResultModifier.py:devn=0.1:db_path="robot-exec-times.db"boxplot=True testcases

# Ausführung mit allen Parametern inkl. Boxplot- und Testbreaker-Modus
# Hinweis: Nicht alle Parameter akzeptieren bereits andere Werte
python3 -m robot --prerebotmodifier perf_analyser/PerfEvalResultModifier.py:stat_func='avg':devn=0.1:db_path="robot-exec-times.db":boxplot=True:testbreaker=True -L info testcases
```
## Screenshot

### Einbindung der Performance-Analyse in die Log-Datei
![](res/example-test-suite-summary.png)

### Testbreaker in der Log-Datei
![](res/example-testbreaker.png)

## Offene Todo's
- Refactoring des Visualizer inkl. Einbindung der PNG#s über relative Pfade

## Quellen
- Robot-Modifizer: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-532
- Alternative Lösung über Listener denkbar: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-625
- https://github.com/robotframework/SeleniumLibrary
