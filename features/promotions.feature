Feature: The promotion service back-end
  As a store manager
  I need a RESTful promotions service
  So that I can manage promotional offers for products effectively

Background:
  Given the following promotions
  | code      | name | start      | expired    | available | whole_store | promo_type    | value |
  | SAVE10    | q    | 2023-06-01 | 2023-12-30 | 100       | True        | 2             |   10  |
  | BUY1GET1  | w    | 2023-07-01 | 2023-12-15 | 50        | False       | 1             |   0   |
  | FREESHIP  | e    | 2023-08-01 | 2023-12-31 | 200       | True        | 1             |  50   |

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
    Then I should see the title "Promotions SAVE10" in detail page
    And I should see "q" in the "fld Name" field in detail page
    And I should see "SAVE10" in the "fld Code" field in detail page
    And I should see "2023-06-01" in the "fld Start" field in detail page
    And I should see "2023-12-30" in the "fld End" field in detail page
    And I should see "100" in the "fld Available" field in detail page
    And I should see "10" in the "fld Val" field in detail page
    And I should see "true" in the "chk Whole Store" field in detail page
    And I should see "2" in the "sel type" dropdown in detail page
    When I set the "fld Name" to "Test2" in detail page
    And I set the "fld Start" to "02-12-2023" in detail page
    And I set the "fld End" to "01-01-2024" in detail page
    And I set the "fld Available" to "50" in detail page
    And I press the "submit" button in detail page
    Then I should see the message "Promotion SAVE10 updated" in toast of detail page
  

Scenario: Revoke a promotion
    When I visit the "Detail Page" for "SAVE10"
    And I press the "Revoke" button in detail page
    When I visit the "Detail Page" for "SAVE10"
    Then I should see warning "Invalid Promotion" in message of detail page

Scenario: Delete a promotion
    When I visit the "Detail Page" for "SAVE10"
    And I press the "Del" button in detail page
    Then I should see "Promotions RESTful Service" in the title
