import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import pandas as pd

# open chrome
driver = webdriver.Chrome()


# main
def main():
    url = "https://www.ebay.com/"

    print("Start")
    print("Scraping Ebay\n")

    driver.get(url)  # Opening the URL.

    # Maximize the screen.
    driver.set_window_size(1024, 600)
    driver.maximize_window()

    clear_cooks()
    product_list = open_excel_file()

    # Loop through the product list
    try:
        for product in product_list:
            search(product)

    except FileNotFoundError:
        print("File not found while searching for product")
    except Exception as e:
        print("An error occurred while searching for product")
        print("Error details:", str(e))
    print("Done")


# Function clears the cookies
def clear_cooks():

    print("Conducted a test search to check for cookies.")
    driver.refresh()
    time.sleep(2)

    # Perform a search test to ensure that the cookies are successfully retrieved.
    try:
        input_search = driver.find_element(By.XPATH, "/html/body/div[3]"
                                                     "/div/header/table/tbody"
                                                     "/tr/td[5]/form/table/tbody"
                                                     "/tr/td[1]/div[1]/div/input[1]")

        input_search.clear()
        input_search.send_keys("test")
        input_search.send_keys(Keys.RETURN)

    except Exception as ew:
        print(f"An error occurred: {str(ew)}")
        driver.quit()

    print("Completed the test search.")

    time.sleep(2)

    # Clicking the accept button to consent to cookies.
    try:
        accept_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "gdpr-banner-accept"))
        )
        accept_button.click()
        print("Clearing cookies...")

    except Exception as ee:
        print(f"An error occurred: {str(ee)}")
        return False
    print("Done, cookies cleared.\n")
    time.sleep(2)


def open_excel_file():

    path = r"C:\\Users\\Eggers\\Desktop\\coding_werk_map\\btmarkt\scraping_bt\\"
    filename = "data_prijzen_Installatiemateriaal_btmarkt.xlsx"
    print("Open Excel and import/load the products.\n")

    xl = pd.read_excel(path + filename)
    print('Displaying the first 5 items.')
    print(xl['Product naam'].head())
    time.sleep(2)
    print()
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
        # Handle error gracefully, for example, logging or raising exception


# Checking if the first search result is a match.
# If there's no match, the function will save no value.
def check_match(match_woord):
    print("Checking for a match between the search and the first result.")

    time.sleep(2)

    wait = WebDriverWait(driver, 10)

    # results = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 's-item__title')))
    results = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 's-item__title')))

    # Extracting the first word from the title to check for a match.
    if len(results) > 1:  # Check if the results page is not empty.
        first_result = results[5]
        title_text = first_result.text.strip()
        print(title_text)
        first_title_word = title_text.split(" ")[0]

    else:
        print("No product search results found.")
        first_title_word = "No value"

    print("First word from product name search:", match_woord)
    print("First word extracted from search result title:", first_title_word)

    is_match = (match_woord.upper() == first_title_word.upper())

    if is_match is True:
        print("Match found.")
        return True
    else:
        print("No match found.")
        return False


#def scrap_data():
    #scrap_data()


if __name__ == '__main__':
    main()
