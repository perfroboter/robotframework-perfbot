## Perfbot - Architekturdokumentation nach arc42

# TODO: Diese Datei ist in Arbeit

## Bausteinsicht

### Ebene 1 - High-Level-Architektur

![](res/architektur_high_level.png)

### Ebene 2 - Komponentendiagramm -  TODO

```plantuml
@startuml

node "Robot Framework" {
    () API
}

node Perfbot {

}

[Perfbot] ..> () API : uses

[Perfbot] ..> () Sqlite3 : uses

database Sqlite3 {

}

@enduml
```

### Ebene 3 - Klassendiagramm

```plantuml
class robot.api.ResultVisitor 
class perfbot.PerfEvalResultModifier 
class perfbot.perfbot #DDDDDD
abstract  perfbot.PersistenceService
class  perfbot.PerfEvalVisualizer
class  perfbot.Sqlite3PersistenceService

perfbot.PerfEvalResultModifier <|-- perfbot.perfbot
robot.api.ResultVisitor <|-- perfbot.PerfEvalResultModifier

perfbot.PerfEvalResultModifier o-- perfbot.PersistenceService
perfbot.PerfEvalResultModifier o-- perfbot.PerfEvalVisualizer
perfbot.PersistenceService <|-- perfbot.Sqlite3PersistenceService

note left of perfbot.perfbot: Starter
```


## Quellen
- https://arc42.org