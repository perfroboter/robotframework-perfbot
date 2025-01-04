*** Settings ***
Library    Browser

*** Variables ***
${SERVER}         localhost:7272
${BROWSER}        chromium
${HEADLESS}        true
${DELAY}          0
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Login Page Should Be Open
    Input Username    demo
    Input Password    mode
    Submit Credentials
    Sleep    20
    Welcome Page Should Be Open
    [Teardown]    Close Browser

*** Keywords ***
Open Browser To Login Page
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    New Page    ${LOGIN URL}

Login Page Should Be Open
    Get Title    equals    Login Page

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Fill Text    id=username_field    ${username}

Input Password
    [Arguments]    ${password}
    Fill Text    id=password_field    ${password}

Submit Credentials
    Click    id=login_button

Welcome Page Should Be Open
    Get Url    *=    ${WELCOME URL}
    Get Title    equals    Welcome Page
