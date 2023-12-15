import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

if __name__ == '__main__':

    driver =  webdriver.Chrome()
    driver.get("https://www.outsystems.com/forge/list?q=&t=&o=most-popular&tr=False&oss=False&c=%205361,5362,5363,5364,5365,5366,5367,5368,5369,5370,5381,5382,5383,5384,5385,5386,5387,5388,5389,5390,5391,3485,5392,5393&a=&v=&hd=False&tn=&scat=forge")
    driver.maximize_window()

    # Create wait object to wait for 20s
    wait = WebDriverWait(driver,20)

    # Click on Accept cookies button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()

    # Click on Load more button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='PortalTheme_wt778_block_wtMainContent_wtLoadMore']"))).click()
    time.sleep(10)

    # Click on Load more button
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='PortalTheme_wt778_block_wtMainContent_wtLoadMore']"))).click()
    time.sleep(10)

    auto = "test"