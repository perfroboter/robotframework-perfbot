*** Settings ***
Suite Setup       Beispiel starten
Documentation     Integrationstest zur Perfbot. Startet die Beispieltests und prüft die log.html und report.html
Library           Process
Library           SeleniumLibrary
Library           OperatingSystem
Suite Teardown    Aufraeumen

*** Variables ***
${LOG_HTML}     file:///Users/lennart/Documents/Development/Studium/2022_Master-Thesis/robot-execution-time/tests/integrationtests/temp/log.html
${BROWSER}      Chrome
${START_SUT}    python3 example/sut/server.py
${RUN_ROBOT}    robot --prerebotmodifier perfbot/perfbot.py:devn=0.1:db_path="tests/integrationtests/temp/test.db":boxplot=True:testbreaker=True --outputdir tests/integrationtests/temp example/tests

*** Test Cases ***
Perfbot im ersten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=NO STATS
Perfbot im zweiten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=1
Perfbot im dritten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=2

*** Keywords ***
Beispiel starten
    Start Process    ${START_SUT}    shell=yes    alias=sut
Beispiel mit Robot testen
    ${result}=	Run Process    ${RUN_ROBOT}    shell=yes
Vorhandensein der Dateien pruefen
    File Should Exist    tests/integrationtests/temp/test.db
    File Should Exist    tests/integrationtests/temp/output.xml
    File Should Exist    tests/integrationtests/temp/log.html
    File Should Exist    tests/integrationtests/temp/report.html
Log-Datei pruefen
    [Arguments]    ${logdatei}=${LOG_HTML}    ${metadata_feld}=Performance Analysis:    ${titel_in_tabelle}= Deviation from avg    ${erster_testfall}=Invalid Username    ${testflauf_anzahl}=1
    Open Browser    ${logdatei}   ${BROWSER}
    Title Should Be    Tests Log
    Click Element    css:div#s1-s1
    Page Should Contain Element    css:div#s1-s1 table
    Table Should Contain    locator=css:div#s1-s1 table    expected=${metadata_feld}
    ${element}=    GetWebElement    locator=xpath://*[@id="s1-s1"]/div[2]/table/tbody/tr[3]/td/table
    Element Should Contain    ${element}    ${titel_in_tabelle}
    Table Cell Should Contain    locator=${element}   row=2    column=1    expected=${erster_testfall}
    Table Cell Should Contain    locator=${element}   row=2    column=6    expected=${testflauf_anzahl}      
    Click Image    //*[@id="s1-s1"]/div[2]/table/tbody/tr[3]/td/p[3]/img
    ${boxplot}=    Get Element Attribute    //*[@id="s1-s1"]/div[2]/table/tbody/tr[3]/td/p[3]/img    src
    Log            Boxplot saved under: ${boxplot}
Aufraeumen
    Terminate All Processes    kill=True
    Remove Directory    tests/integrationtests/temp    recursive=True
    