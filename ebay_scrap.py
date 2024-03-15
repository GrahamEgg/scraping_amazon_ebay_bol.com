import time
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup


# open chrome
driver = webdriver.Chrome()
title_list = []
price_list = []
file = sys.argv[1]


# main
def main():

    url = "https://www.ebay.com/"

    print("Start")
    print("Scraping Ebay\n")

    driver.get(url)  # Opening the URL.

    # Maximize the screen.
    driver.set_window_size(1024, 600)
    driver.maximize_window()

    driver.refresh()

    clear_cooks()

    product_list = open_excel_file(file)
    print("found", len(product_list), "products\n")

    # Loop through the product list
    try:
        for product in product_list:
            search(product)

    except FileNotFoundError:
        print("File not found while searching for product")
    except Exception as e:
        print("An error occurred while searching for product")
        print("Error details:", str(e))

    print(title_list)
    print(price_list)
    print(len(title_list))
    print(len(price_list))

    print("Done")


# Function clears the cookies
def clear_cooks():
    # Checking for the "cookies" element
    try:
        driver.switch_to.default_content()
        accept_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "gdpr-banner-accept"))
        )
        # If the 'cookies' element is not found, we will conduct a test search.
    except TimeoutException:
        print("No cookie element found")
        print("Conducted a test search to check for cookies.")

        # Perform a search test to ensure that the cookies are successfully retrieved.
        try:
            input_search = driver.find_element(By.ID, "gh-ac")
            input_search.clear()
            input_search.send_keys("test")
            input_search.send_keys(Keys.RETURN)
            print("Completed the test search.")

            # If there are still no cookies, it will continue without clicking the button.

            accept_button = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.ID, "gdpr-banner-accept"))
            )
        except TimeoutException:
            print("No cookies found, proceed with scraping")
        else:
            accept_button.click()
            print("Clearing cookies...")
    else:
        accept_button.click()
        print("Clearing cookies...")
    print("Done, cookies cleared.\n")


def open_excel_file(path_filename):
    print("Open Excel and import/load the products.\n")
    # open excel file with panda
    xl = pd.read_excel(path_filename)
    print('Displaying the first 5 items.')
    print(xl['Product naam'].head())
    time.sleep(2)
    print()
    # make al list of item from product naam
    return xl['Product naam'].tolist()


# Select the search bar and enter the given product for searching.
def search(product_name):

    print("Initiating search for:", product_name)
    # Extracting the first word from the product name to verify search results.
    first_product_name = product_name.split(" ")[0]

    # Selecting the search bar and inputting the product name.
    try:
        input_search = driver.find_element(By.ID, "gh-ac")
        input_search.clear()
        input_search.send_keys(product_name)
        input_search.send_keys(Keys.RETURN)
        print("Search performed successfully.\n")
        time.sleep(2)

        # Checking for a match.
        check_match(first_product_name)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Checking if the first search result is a match.
# If there's no match, the function will save no value.
def check_match(match_woord):
    print("Checking for a match between the search and the first result.")

    url = driver.current_url
    pagina = requests.get(url)
    pagina.raise_for_status()

    soup = BeautifulSoup(pagina.content, 'html.parser')

    # It will first check if a complete match is found.
    ul_result = soup.find('ul', class_="srp-results srp-list clearfix")
    if ul_result:
        super_result = ul_result.find('li', class_="s-item s-item__before-answer s-item__pl-on-bottom")
        if super_result:

            # Will skips the sponsored items.
            spon_element = super_result.find('span', class_='s-item__sep')
            if not (spon_element and 'Sponsored' in spon_element.get_text()):

                # Check whether there is a product title.
                # and strips text
                product_title = super_result.find('div', class_="s-item__title")
                text_content = product_title.text.strip() if product_title else "no value"

                # Check whether there is a product price.
                product_price = super_result.find('span', class_="s-item__price")

                # Replace spaces and dollar signs.
                price_content = product_price.text.strip().replace('\n', '')\
                    .replace('  ', '').replace('$', '') if product_price else "no value"

            else:
                text_content = "no value"
                price_content = 0

        else:
            results = soup.find_all(class_='s-item__wrapper clearfix')
            text_content, price_content = get_data(results)

    else:
        results = soup.find_all(class_='s-item__wrapper clearfix')
        text_content, price_content = get_data(results)

    first_title_word = text_content.split(" ")[0]

    is_match = (match_woord.upper() == first_title_word.upper())

    if is_match is True:
        title_list.append(text_content)
        price_list.append(float(price_content))
        print("Match found.\n")

    else:
        text_content = "no value"
        title_list.append(text_content)
        price_list.append(float(0))
        print("No match found.\n")
        return False


# If it's not a perfect match, it will check if it's not empty
# Then, it will search for the first match after the sponsors.
def get_data(results):
    # checking if result is not empty
    text_content = "No value"
    price_content = 0

    if len(results) > 1:
        print("ss")
        for result in results:
            spon_element = result.find('span', class_='s-item__sep')
            if not (spon_element and 'Sponsored' in spon_element.get_text()):
                product_title = result.find('div', class_="s-item__title")
                text_content = product_title.text.strip() if product_title else "no value"

                product_price = result.find('span', class_="s-item__price")
                price_content = product_price.text.strip().replace('\n', '') \
                    .replace('  ', '').replace('$', '') if product_price else "no value"
                break
    else:
        text_content = "No value"
        price_content = 0

    return text_content, price_content


if __name__ == '__main__':
    main()
