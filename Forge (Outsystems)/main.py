# Some testing for the outsystems / https://www.outsystems.com/forge/list on Selenium

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def open_browser(path) -> selenium.webdriver:
    driver = webdriver.ChromeOptions()
    driver.add_argument('--no-sandbox')
    browser = webdriver.Chrome()
    browser.get(path)
    return browser


def quit_browser(browser):
    browser.quit()


def browser_find_elements(driver):
    # Create wait object to wait for 20s
    driver.maximize_window()

    # Create wait object to wait for 100s
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    wait = WebDriverWait(driver, 200, ignored_exceptions=ignored_exceptions)

    # Click on Accept cookies button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()

    # Click on Load more button
    for i in range(2):
        print('Iteration: ' + str(i))
        for j in range(2):
            wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='PortalTheme_wt778_block_wtMainContent_wtLoadMore']"))).click()
            # time.sleep(10)
    description = driver.find_elements(By.XPATH, '//*[@id="PortalTheme_wt778_block_wtMainContent_wtResults"]')

    # add_missing_information_from_component_page(driver, 10)

    rows = split_text_into_rows(description[0].text)
    test = 'String'
    string_splitter_into_excl_file(rows)
    # time.sleep(100)
    print(description[0].text)

def split_text_into_rows(text):
    # Component name, Description, Number of Ratings, Number of Downloads, Supported
    list_of_substrings = text.split("\n")
    # 5 items long, first item is the naming:
    component_array = []
    components = []
    counter = 0;
    for substring in list_of_substrings:
        components.append(substring)
        counter += 1
        # One string contains an error in the text file where the descriptions is messed up with a line seperator.
        # This string has to be append to the second field before reiterating over the other string
        if counter == 3:
            if not contains_only_digits(substring):
                components[1].join(substring)
                components[2] = ''
                counter = 2

        if counter == 4:
            component_array.append(components)
            components = []
            counter = 0

    return component_array


def string_splitter_into_excl_file(rows):
    import pandas as pd
    import openpyxl

    df = pd.DataFrame(rows)

    excel_file_path = '/Users/jonas/Desktop/Bachelor-Thesis/Papers/Data Forge Outsystems.xlsx'

    df.to_excel(excel_file_path, index=False)


def contains_only_digits(s):
    return s.isdigit()

def add_missing_information_from_component_page(brwoser, number_of_components, original):
    component_xpath_first = '//*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl'
    component_xpath_second = '_GriderCSSGrid_wt43_block_wtContent_Forge_Pat_wt351_block_wtHoverItem_wtLnk_Detail"]'
    answers = []
    for i in range(0, 10, 2):
        component_xpath_number = "{:02d}".format(i)
        component_xpath = component_xpath_first + component_xpath_number + component_xpath_second
        component_details = open_component_page(browser, component_xpath)
        answers.append(component_details)


# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl00_GriderCSSGrid_wt43_block_wtContent"]
# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl04_GriderCSSGrid_wt43_block_wtContent"]
# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl06_GriderCSSGrid_wt43_block_wtContent"]

# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl00_GriderCSSGrid_wt43_block_wtContent_Forge_Pat_wt351_block_wtHoverItem_wtLnk_Detail"]
# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl02_GriderCSSGrid_wt43_block_wtContent_Forge_Pat_wt351_block_wtHoverItem_wtLnk_Detail"]
# //*[@id="PortalTheme_wt778_block_wtMainContent_wtForgeProjectList_ctl04_GriderCSSGrid_wt43_block_wtContent_Forge_Pat_wt351_block_wtHoverItem_wtLnk_Detail"]

# Categories
# //*[@id="PortalTheme_wt3_block_wtMainContent_wt7_Forge_Pat_wt118_block_wtContent_Forge_Pat_wt190_block_wtContent"]/div[2]/div[1]/div[2]/div
# Number of rating
# //*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent_Forge_CW_wtVotesInfo_block_PortalCommon_Patterns_wt45_block_wtContent_wtNumberOfVotes"]
# Avg Rating
# //*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent_Forge_CW_wtVotesInfo_block_PortalCommon_Patterns_wt45_block_wtContent"]/div[2]
# Number of reviews
# //*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent"]/div[3]
# Compatible with Version
# //*[@id="PortalTheme_wt3_block_wtMainContent_wt7_Forge_Pat_wt118_block_wtContent_Forge_Pat_wt190_block_wtContent_Forge_CW_wt46_block_wtMajorsRecordList_ctl00_wt25_wtPlatformVersions"]
# Supported / Trusted / Neither of them (worst case just hit the numbers),
# -> Already covered through initial data retrieval
def open_component_page(browser, componentstring):
    wait = WebDriverWait(browser, 100)

    # Click on Accept cookies button
    wait.until(EC.element_to_be_clickable((By.XPATH,componentstring))).click()

    categories = browser.find_elements(By.XPATH,
                                       '//*[@id="PortalTheme_wt3_block_wtMainContent_wt7_Forge_Pat_wt118_block_wtContent_Forge_Pat_wt190_block_wtContent"]/div[2]/div[1]/div[2]/div')[0].text
    number_of_rating = browser.find_elements(By.XPATH,
                                        '//*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent_Forge_CW_wtVotesInfo_block_PortalCommon_Patterns_wt45_block_wtContent_wtNumberOfVotes"]')[0].text
    avg_rating = browser.find_elements(By.XPATH,
                                        '//*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent_Forge_CW_wtVotesInfo_block_PortalCommon_Patterns_wt45_block_wtContent"]/div[2]')[0].text
    number_of_reviews = browser.find_elements(By.XPATH,
                                        '//*[@id="PortalTheme_wt3_block_wtMainContent_wt7_wtHeader_Forge_Pat_wtComponentDetailHeader_block_wtContentFooter_wtContentFooter_wtHeader_ContentFooter_wtHeader_FooterSection_Desktop_Forge_Pat_wt5_block_wtContent"]/div[3]')[0].text
    compatible_with_version = browser.find_elements(By.XPATH,
                                        '//*[@id="PortalTheme_wt3_block_wtMainContent_wt7_Forge_Pat_wt118_block_wtContent_Forge_Pat_wt190_block_wtContent_Forge_CW_wt46_block_wtMajorsRecordList_ctl00_wt25_wtPlatformVersions"]')[0].text
    return [categories, number_of_rating, avg_rating, number_of_reviews, compatible_with_version]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = 'https://www.outsystems.com/forge/list?q=&t=&o=most-popular&tr=False&oss=False&c=%205406,5407,5408,5409,5410,5411,5412,5413,5414&a=&v=&hd=False&tn=&scat=forge'
    browser = open_browser(path)
    browser_find_elements(browser)
    quit_browser(browser)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
