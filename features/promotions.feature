Feature: The promotion service back-end
  As a store manager
  I need a RESTful promotions service
  So that I can manage promotional offers for products effectively

Background:
  Given the following promotions
    | code      | name        | start      | expired    | available | whole_store | promo_type    |
    | SAVE10    | promo_s10   | 2023-06-01 | 2023-06-30 | 100       | True        | 20            |
    | BUY1GET1  | promo_b1g1  | 2023-07-01 | 2023-07-15 | 50        | False       | 30            |
    | FREESHIP  | promo_free  | 2023-08-01 | 2023-08-31 | 200       | True        | 50            |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Promotions RESTful Service" in the title
  And I should not see "404 Not Found"

Scenario: Creating a new promotion
    When I visit the "Home Page"
    And I set the "Code" to "SUMMER2022"
    And I set the "Name" to "promo_50"
    And I set the "Start" to "06-01-2022"
    And I set the "Expired" to "09-09-2022"
    And I set the "Available" to "100"
    And I select "True" in the "WholeStore" dropdown
    And I select "50%" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Promotion created successfully"

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


Scenario: delete a promotion
    When I visit the "Home Page"
    And I set the "Code" to "SAVE10"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "SAVE10" in the "Code" field
    And I should see "promo_s10" in the "Name" field
    And I should see "100" in the "Available" field
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


