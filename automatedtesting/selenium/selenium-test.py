# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import logging

def login(user, password):
    logging.basicConfig(filename="./selenium.log", format="%(asctime)s %(message)s", filemode="w", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    logging.info('Starting the browser...')

    options = ChromeOptions()

    options.add_argument("--headless") 
    options.add_argument('--no-sandbox')
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options)
    logging.info('Logging in...')
    driver.get('https://www.saucedemo.com/')

    # login
    driver.find_element(By.CSS_SELECTOR, "input[id='user-name']").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    product_label = driver.find_element(By.CSS_SELECTOR, "span.title").text

    assert "Products" in product_label
    logging.info('Login successfully with username: {:s} and password: {:s}'.format(user, password))

    return driver

def add_cart(driver, totalItem):
    for i in range(totalItem):
        # Get URL
        element = "a[id='item_" + str(i) + "_title_link']"
        # Find URL
        driver.find_element(By.CSS_SELECTOR, element).click()
        # Add product
        driver.find_element(By.CSS_SELECTOR, "button.btn_primary.btn_inventory").click()
        # Get product's name
        product = driver.find_element(By.CSS_SELECTOR, "div.inventory_details_name").text
        # Logging
        logging.info(product + " was added to shopping cart.")
        # Back to main site
        driver.find_element(By.CSS_SELECTOR, "button.inventory_details_back_button").click()
    logging.info('{:d} items were added to shopping cart.'.format(totalItem))

def remove_cart(driver, totalItem):
    for i in range(totalItem):
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element(By.CSS_SELECTOR, element).click()
        driver.find_element(By.CSS_SELECTOR, "button.btn_secondary.btn_inventory").click()
        product = driver.find_element(By.CSS_SELECTOR, "div.inventory_details_name").text
        logging.info(product + "Removed from shopping cart item name:" +product)
        driver.find_element(By.CSS_SELECTOR, "button.inventory_details_back_button").click()
        logging.info('{:d} items are all removed from shopping cart.'.format(totalItem))

if __name__ == "__main__":
    numberOfItem = 6
    TEST_USER = 'standard_user'
    TEST_PASS = 'secret_sauce'
    driver = login(TEST_USER, TEST_PASS)
    add_cart(driver, numberOfItem)
    remove_cart(driver, numberOfItem)
    logging.info('Test Selenium UI completed')