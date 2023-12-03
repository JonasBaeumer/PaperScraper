# Some testing for the outsystems / https://www.outsystems.com/forge/list on Selenium
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def open_browser(path) -> selenium.webdriver:
    browser = webdriver.Firefox()
    browser.get(path)
    return browser


def quit_browser(browser):
    browser.quit()


def browser_find_elements(browser):
    description = browser.find_elements(By.XPATH, '/html/body/form/div[3]/div[1]/div[1]/div[1]/div/div/div[1]/div[1]/div[2]')
    test = 'String'
    #time.sleep(100)
    print(description[0].text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = 'https://www.outsystems.com/forge/component-overview/1385/outsystems-ui'
    browser = open_browser(path)
    browser_find_elements(browser)
    quit_browser(browser)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
