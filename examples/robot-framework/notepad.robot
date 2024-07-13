*** Settings ***
Library    RPALite

*** Test Cases ***
Notepad Test
    Run Command    notepad.exe
    Click By Text    Notepad
    Input Text    This is a demo using RPALite.
    ${app} =     Find Application    .*Notepad
    Close App    ${app}