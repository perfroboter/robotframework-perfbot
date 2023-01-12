# Proof-of-Concept: Robot-Testfälle als Indikator für Performance-Probleme nutzen

## Idee

Mittels Modifizer wird während der Laufzeit die aktuelle Testdauer jedes Testfalls analyisiert und mit einem Maximalwert und dem Durchschnitt der letzten Läufe der Vergangenheit verglichen. Lässt sich daraus ein Performanzproblem erkennen, so wir der Testfall auf Fehlerhaft gesetzt und mit einer Message ausgestattet.

## Architektur

- `modifier/ExecutionTimeChecker.py`: Programm, welches im Hintergrund die aktuellen Laufzeit zu jedem Testfall evaluiert
- `sqlite` Installationsskript zur Anlage der sqlite3-Datenbank

## Quick Start
```bash
# Parameterliste: max_seconds (Absolutes Maximum für jeden Testfall (hier 5 Sekunden)), max_deviation_from_last_runs (Prozentuale Abweichung von den zurückliegenen Ausführungen), last_n_runs (Beschränkung auf die letzten N Laufzeiten (noch nicht implementiert))
robot --prerebotmodifier modifier/ExecutionTimeChecker.py:5 -L info testcases
```
Hinweis: `prerebotmodifier` wird nach der Testausführung basierend auf dem Result-Modell ausgeführt und verändert die report.html, jedoch nicht die output.xml (vgl. Robot-Docs 3.6.9).


## Quick Start - Neu
```bash
# Starten des System-under-Test
python3 sut/server.py
# Ausführung der beispielhaften Tests ohne PerfEval
# Vorher: Installationsanleitung gemäß https://github.com/robotframework/SeleniumLibrary
python3 -m robot testcases
# Ausführung der Tests mit PerfEval als ResultModifier
# Erläuterung: Der ResultModifier läuft nach der Ausführung aller Tests und verändert nur die log.html und report.html
python3 -m robot --prerebotmodifier perf_analyser/PerfEvalResultModifier.py -L info testcases

```


## Screenshot

![](example_result.png)

## Quellen
- Robot-Modifizer: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-532
- Alternative Lösung über Listener denkbar: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-625
- https://github.com/robotframework/SeleniumLibrary
