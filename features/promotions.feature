Feature: The promotion service back-end
  As a store manager
  I need a RESTful promotions service
  So that I can manage promotional offers for products effectively

Background:
  Given the following promotions
  | code      | name | start      | expired    | available | whole_store | promo_type    |
  | SAVE10    | q    | 2023-06-01 | 2023-06-30 | 100       | True        | 20            |
  | BUY1GET1  | w    | 2023-07-01 | 2023-07-15 | 50        | False       | 30            |
  | FREESHIP  | e    | 2023-08-01 | 2023-08-31 | 200       | True        | 50            |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Promotions RESTful Service" in the title
  And I should not see "404 Not Found"

Scenario: Creating a new promotion
    When I visit the "Home Page"
    And I set the "Code" to "SUMMER2022"
    And I set the "Name" to "c"
    And I set the "Start" to "06-01-2022"
    And I set the "Expired" to "09-09-2022"
    And I set the "Available" to "100"
    And I select "True" in the "WholeStore" dropdown
    And I select "50%" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Promotion created successfully"

Scenario: Update a existing promotion
    When I visit the "Detail Page" for "SAVE10"
    Then I should see "Promotions SAVE10" in the title of detail page
    When I set the "Code" to "SAVE10" in the detail page
    And I set the "Name" to "q" in the detail page
    And I set the "Start" to "12-01-2023" in the detail page
    And I set the "End" to "12-03-2023" in the detail page
    And I set the "Available" to "100" in the detail page
    And I select "True" in the "WholeStore" dropdown in the detail page
    And I select "20%" in the "Type" dropdown in the detail page

