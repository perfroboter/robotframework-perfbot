# Testplan

## Teststrategie

Die Qualität von Perfbot soll einerseits durch statsiche und dynamische Tests beurteilt werden. Alle Tests sind dabei automatisiert, um bei jeder Änderung die Regressionstestsuite (Unit- und Integrationstests) durchzuführen.

## Statische Code-Analyse

### Komplexitätsanalyse mit radon

Mittels Radon wird die Komplexität des Codes analysiert. Die Aussage über die Komplexität soll genutzt werden, um einerseits dort, wo es sinnvoll ist, die Komplexität zu reduzieren, anderseits gibt es Orientierung, wo mehr Unit-Tests sinnvoll sind.
```bash
python3 -m radon cc perfbot/* -a -s
```
Je komplexer der Code, desto mehr Unit-Tests.

## Unittests

Der Pythoncode wird mittels Unittests (Python-Modul `unittest`) getestet. Für jede Klasse sind dabei Tests abgelegt.

```bash
python3 -m unittest discover perfbot/tests "test_.py"
```

## Integrationstest (Smoke-Test)

Der Integrationstest im Sinne eines Smoke-Tests führt die Robot-Testfälle des Selenium-Beispiels (`example`) inkl. Ausführung von Perfbot durch und prüft im Anschluss, ob in der `log.html` die Informationen von Perfbot zu finden sind.
Dabei werden drei Durchläufe gemacht, um sowohl die initale Anlage der Datenbank, als auch den Rückgriff auf historischen Daten zu prüfen.

```bash
# Ausführung aus Root-Ordner des Repos
python example/sut/server.py #SUT vorher starten 
 
```