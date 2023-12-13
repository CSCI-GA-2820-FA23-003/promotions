######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
import time
from behave import when, then
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC


@when('I visit the "Detail Page" for "{promotion_id}"')
def visit_detail_page(context, promotion_id):
    """Make a call to the Detail URL"""
    context.driver.get(context.base_url + "/promotions/" + promotion_id + "/edit")
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')


@then('I should see the title "{message}" in detail page')
def check_title(context, message):
    """Check the document title for a message"""
    # Now assert that the title is as expected
    assert message == context.driver.title


@when('I set the "{element_name}" to "{text_string}" in detail page')
def set_text(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "-")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)
    print(f"Element value: {element.get_attribute('value')}")  # Debug print


@when('I select "{text}" in the "{element_name}" dropdown in detail page')
def set_select(context, text, element_name):
    # Generate the element ID
    element_id = element_name.lower().replace(" ", "-")
    # print(f"Dropdown ID: {element_id}")  # Debug print

    # Find the dropdown element
    dropdown_element = context.driver.find_element(By.ID, element_id)
    # print(f"Dropdown element found: {dropdown_element}")  # Debug print

    # Create a Select object
    select = Select(dropdown_element)
    # print(f"Select object created: {select}")  # Debug print

    # Select the option by visible text
    select.select_by_visible_text(text)
    # print(f"Option selected: {text}")  # Debug print


@when("I select product list in detail page")
def set_select(context):
    select_root = context.driver.find_element(By.ID, "product-select")
    select_root.click()


@when('I select product "{id}" from list in detail page')
def set_select(context, id):
    elements = context.driver.find_element(
        By.CSS_SELECTOR, f".item.product[data-value='{id}']"
    )
    assert elements
    print(f"ELEMENTS: {elements.text}")
    elements.click()


@when('I create product "{id}" from list in detail page')
def set_select(context, id):
    select_root = context.driver.find_element(By.ID, "product-select")
    search = select_root.find_element(By.CSS_SELECTOR, ".search")
    search.send_keys(id)
    search.send_keys(Keys.ENTER)
    select_root.send_keys(Keys.ENTER)


@when('I remove product "{id}" from list in detail page')
def delete_product(context, id):
    product = context.driver.find_element(
        By.CSS_SELECTOR, f".label.visible[data-value='{id}']"
    )
    delete_product = product.find_element(By.CSS_SELECTOR, ".delete.icon")
    delete_product.click()


@when('I wait for "{seconds}" seconds in detail page')
def wait_seconds(context, seconds):
    time.sleep(int(seconds))


@then('I should see product "{id}" in list in detail page')
def check_product(context, id):
    product = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, f".item.product[data-value='{id}']")
        )
    )
    assert product and product.text == id


@then('I should not see product "{id}" in list in detail page')
def check_product(context, id):
    product = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR, f".item.product[data-value='{id}']")
        )
    )
    assert not product or product.text != id


@then('I should see product "{id}" selected in detail page')
def check_product(context, id):
    product = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, f".label.visible[data-value='{id}']")
        )
    )
    assert product and product.text == id


@then('I should not see product "{id}" selected in detail page')
def check_product(context, id):
    product = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, f".label.visible[data-value='{id}']")
        )
    )
    assert not product or product.text != id


@then('I should see "{value}" in the "{element_name}" dropdown in detail page')
def check_select(context, value, element_name):
    element_id = element_name.lower().replace(" ", "-")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.get_dom_attribute("value") == value


@then('the "{element_name}" field should equal "{text_string}" in detail page')
def check_text_equal(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == text_string


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################


@when('I press the "{button}" button in detail page')
def press_btn(context, button):
    button_id = "btn-" + button.lower()
    context.driver.find_element(By.ID, button_id).click()


@then('I should see "{name}" in the results in detail page')
def check_res(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"), name
        )
    )
    assert found


@then('I should not see "{name}" in the results in detail page')
def check_not_res(context, name):
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text


@then('I should see the message "{message}" in toast of detail page')
def check_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, ".toast-container .message")
        )
    )
    if found.text != message:
        print(f"Toast message: {found.text}")  # Debug print
    assert found and found.text == message


@then('I should see warning "{message}" in message of detail page')
def check_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.visibility_of_element_located(
            (By.ID, "error-invalid-title")
        )
    )
    print(f"Toast message: {found.text}")
    assert found and found.text == message


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################


@then('I should see "{text_string}" in the "{element_name}" field in detail page')
def check_text(context, text_string, element_name):
    element_id = element_name.lower().replace(" ", "-")
    print(f"Element ID: {element_id}")  # Debug print
    print(
        f"Element value: {context.driver.find_element(By.ID, element_id).get_attribute('value')}"
    )  # Debug print
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    assert found


@when('I change "{element_name}" to "{text_string}" in detail page')
def change_text(context, element_name, text_string):
    element_id = element_name.lower().replace(" ", "-")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
