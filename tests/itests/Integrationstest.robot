*** Settings ***
Suite Setup       Vorbereiten
Documentation     Integrationstest zur Perfbot. Startet die Beispieltests und prüft die log.html und report.html. Vorm Starten den Ablageort der LOG_HTML anpassen.
Library           Process
Library           SeleniumLibrary
Library           OperatingSystem
Suite Teardown    Aufraeumen

*** Variables ***
${BROWSER}      Chrome
${START_SUT}    python3 example/sut/server.py
${RUN_ROBOT}    python3 -m robot --prerebotmodifier perfbot.perfbot:devn=0.1:db_path="tests/itests/temp/test.db":boxplot=True:testbreaker=True:boxplot_folder="tests/itests/temp/" -o tempoutput.xml -l templog.html -r tempreport.html example/tests

*** Test Cases ***
Perfbot im ersten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=NO STATS
    # beim ersten Durchlauf gibt es noch keinen Boxplot
    Close Browser
Perfbot im zweiten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=1
    Boxplot in Log-Datei und lokal pruefen
    Close Browser
Perfbot im dritten Durchlauf testen
    Beispiel mit Robot testen
    Vorhandensein der Dateien pruefen
    Log-Datei pruefen    testflauf_anzahl=2
    Boxplot in Log-Datei und lokal pruefen
    Close Browser

*** Keywords ***
Vorbereiten
    Remove Directory    tests/itests/temp    recursive=True
    Create Directory    tests/itests/temp
    Beispiel SUT starten
    ${pwd}=	Run Process    pwd    shell=yes
    Log    pwd: ${pwd.stdout}
    Set Global Variable    ${LOG_HTML}    file://${pwd.stdout}/templog.html
    Log    Ablageort der LOG-HTML ermittelt: ${LOG_HTML}
Beispiel SUT starten
    Start Process    ${START_SUT}    shell=yes    alias=sut
Beispiel mit Robot testen
    ${result}=	Run Process    ${RUN_ROBOT}    shell=yes
Vorhandensein der Dateien pruefen
    File Should Exist    tests/itests/temp/test.db
    File Should Exist    tempoutput.xml
    File Should Exist    templog.html
    File Should Exist    tempreport.html
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

Boxplot in Log-Datei und lokal pruefen
        Click Image    //*[@id="s1-s1"]/div[2]/table/tbody/tr[3]/td/p[3]/img
        ${pic}=    Get Element Attribute    //*[@id="s1-s1"]/div[2]/table/tbody/tr[3]/td/p[3]/img    src
        Log        Boxplot saved under: ${pic}
        ${file}=   Evaluate    '${pic}'.replace('file://','')
        File Should Exist    ${file}
Aufraeumen
    Terminate All Processes    kill=True
    Remove Directory    tests/itests/temp    recursive=True
    Remove File         tempoutput.xml
    Remove File         templog.html
    Remove File         tempreport.html
    