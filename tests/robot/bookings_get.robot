*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://localhost:8000

*** Test Cases ***
GET /bookings vrati status 200
    ${response}=    GET    ${BASE_URL}/bookings
    Status Should Be    200    ${response}

GET /bookings vrati zoznam
    ${response}=    GET    ${BASE_URL}/bookings
    ${body}=    Set Variable    ${response.json()}
    Should Not Be Empty    ${body}
