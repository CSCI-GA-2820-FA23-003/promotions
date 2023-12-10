Feature: The promotion service back-end
  As a store manager
  I need a RESTful promotions service
  So that I can manage promotional offers for products effectively

Background:
  Given the following promotions
    | code      | name        | start      | expired    | available | whole_store | promo_type | value |
    | SAVE10    | promo_s10   | 2023-06-01 | 2023-06-30 | 100       | True        | 1          | 20    |
    | BUY1GET1  | promo_b1g1  | 2023-07-01 | 2023-07-15 | 50        | False       | 2          | 30    |
    | FREESHIP  | promo_free  | 2023-08-01 | 2023-08-31 | 200       | True        | 3          | 50    |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Promotions RESTful Service" in the title
  And I should not see "404 Not Found"

Scenario: Creating a new promotion
    When I visit the "Home Page"
    And I set the "Code" to "SUMMER2022"
    And I set the "Name" to "promo_50"
    And I set the "Start" to "09-01-2023"
    And I set the "Expired" to "12-01-2023"
    And I set the "Available" to "100"
    And I select "True" in the "WholeStore" dropdown
    And I select "Buy _ Get 1 Free" in the "Type" dropdown
    And I set the "Value" to "1"
    And I press the "Create" button
    Then I should see the message "Promotion created successfully"
    And I should see "SUMMER2022" in the "Code" field
    And I should see "promo_50" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "2023-09-01" in the "Start" field
    And I should see "2023-12-01" in the "Expired" field
    And I should see "Buy _ Get 1 Free" in the "Type" dropdown
    And I should see "1" in the "Value" field

Scenario: List all promotions
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "promo_s10" in the results
    And I should see "promo_b1g1" in the results
    And I should see "promo_free" in the results
    And I should not see "promo_b3g3" in the results

Scenario: Search via Promotion Code
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Code" field
    And I press the "Clear" button
    Then the "Code" field should be empty
    And the "Name" field should be empty      
    And the "Available" field should be empty                               
    When I paste the "Code" field
    And I press the "Search" button   
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "Percentage" in the "Type" dropdown
    And I should see "2023-06-01" in the "Start" field
    And I should see "2023-06-30" in the "Expired" field
    And I should see "20" in the "Value" field

Scenario: delete a promotion
    When I visit the "Home Page"
    And I set the "Code" to "SAVE10"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "Percentage" in the "Type" dropdown
    And I should see "2023-06-01" in the "Start" field
    And I should see "2023-06-30" in the "Expired" field
    And I should see "20" in the "Value" field
    When I press the "Delete" button
    Then I should see the message "Promotion has been Deleted!"
    And the "Code" field should be empty
    And the "Name" field should be empty      
    And the "Available" field should be empty

Scenario: Retrieve a promotion
    When I visit the "Home Page"
    And I set the "Code" to "SAVE10"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "Code" field should be empty
    When I paste the "ID" field
    When I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "Percentage" in the "Type" dropdown
    And I should see "2023-06-01" in the "Start" field
    And I should see "2023-06-30" in the "Expired" field
    And I should see "20" in the "Value" field

Scenario: Query a Promotion by name
    When I visit the "Home Page"
    And I set the "Name" to "promo_s10"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "Percentage" in the "Type" dropdown
    And I should see "2023-06-01" in the "Start" field
    And I should see "2023-06-30" in the "Expired" field
    And I should see "20" in the "Value" field

Scenario: Search via Promotion Available
    When I visit the "Home Page"
    And I set the "Available" to "100"
    And I press the "Search" button   
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
    And I should see "True" in the "WholeStore" dropdown
    And I should see "Percentage" in the "Type" dropdown
    And I should see "2023-06-01" in the "Start" field
    And I should see "2023-06-30" in the "Expired" field
    And I should see "20" in the "Value" field

Scenario: Update a existing promotion
    When I visit the "Detail Page" for "SAVE10"
    Then I should see the title "Promotions SAVE10" in detail page
    And I should see "promo_s10" in the "fld Name" field in detail page
    And I should see "SAVE10" in the "fld Code" field in detail page
    And I should see "2023-06-01" in the "fld Start" field in detail page
    And I should see "2023-06-30" in the "fld End" field in detail page
    And I should see "100" in the "fld Available" field in detail page
    And I should see "20" in the "fld Val" field in detail page
    And I should see "true" in the "chk Whole Store" field in detail page
    And I should see "1" in the "sel type" dropdown in detail page
    When I set the "fld Name" to "promo_S10" in detail page
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
