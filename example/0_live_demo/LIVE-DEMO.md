# Guide zur Live-Demo auf der Robocon 2025

## Vorbereitung

- Alle Sonstigen Anwendungen (außer PowerPoint und VSCode) sind geschlossen
- VSCode ist geöffnet mit Ordner "Example" im perfbot-Repo
- Python-Server als System-under-Test ist im seperaten Terminal gestartet: `python3 sut/server.py`
- Der Testfall bzw. die Testsuite `valid_login.robot` ist geöffnet
    - Ein Sleep-Step ist auskommentiert
- Das Terminal ist geöffnet
- Der Zoom ist in ausreichender Größe eingestellt
- Der Browser mit dem System-under-Test ist geöffnet: [Login-Page](http://localhost:7272)

## Schritt 1: System-under-Test und Testfälle zeigen
- Test-Login-Seite zeigen
- Beispiel-Testfall zeigen

## Schritt 2: Robot inkl. Perfbot starten per CLI
- Testfälle starten
```bash
robot --prerebotmodifier perfbot.perfbot tests/
```
- log.html in VSCode per Rechtsklick "Open in Default-Browser" öffnen
- Tabelle zeigen
- Boxplot erläutern

## Schritt 3: Fehler injektieren und Perfbot erneut starten
- Sleep in `valid_login.robot` schreiben bzw. einkommentieren
- Erneut starten mit Optionen: 
    - Datenbank angeben
    - Abweichung angeben
    - Testbreaker aktivieren
    - nur lesen drauf zu greifen
```bash
robot --prerebotmodifier perfbot.perfbot:devn=0.5:db_path="robot-exec-times.db":testbreaker=True:readonly=True tests/
```
