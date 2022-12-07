# Proof-of-Concept: Robot-Testfälle als Indikator für Performance-Probleme nutzen

## Idee

Mittels Modifizer wird während der Laufzeit die aktuelle Testdauer jedes Testfalls analyisiert und mit einem Maximalwert und dem Durchschnitt der letzten Läufe der Vergangenheit verglichen. Lässt sich daraus ein Performanzproblem erkennen, so wir der Testfall auf Fehlerhaft gesetzt und mit einer Message ausgestattet.

## Architektur

- `modifier/ExecutionTimeChecker.py`: Programm, welches im Hintergrund die aktuellen Laufzeit zu jedem Testfall evaluiert
- `mysql` SQL-Skripte zur MySQL-Datenbank: Enthällt Tabelle mit den zurückliegenden Testläufen und deren Laufzeiten

## Quick Start
```bash
# Parameterliste: max_seconds (Absolutes Maximum für jeden Testfall (hier 5 Sekunden)), max_deviation_from_last_runs (Prozentuale Abweichung von den zurückliegenen Ausführungen), last_n_runs (Beschränkung auf die letzten N Laufzeiten (noch nicht implementiert))
robot --prerebotmodifier modifier/ExecutionTimeChecker.py:5 -L info testcases
```

## Screenshot

![](example_result.png)

## Quellen
- Robot-Modifizer: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-532
- Alternative Lösung über Listener denkbar: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#toc-entry-625