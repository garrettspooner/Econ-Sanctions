from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas
import time
import os

cwd = os.getcwd()
directory = os.path.dirname(cwd)
parent = os.path.join(directory, "chromedriver")
dict = {}

def scrape(url, file):

    def scroll_to_bottom(driver):
        old_position = 0
        new_position = None
        while new_position != old_position:
            old_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
            time.sleep(1)
            driver.execute_script((
                    "var scrollingElement = (document.scrollingElement ||"
                    " document.body);scrollingElement.scrollTop ="
                    " scrollingElement.scrollHeight;"))
            new_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))

    # service = Service(executable_path=parent)
    # chrome_driver = webdriver.Chrome(service=service)
    chrome_driver = webdriver.Chrome()

    with chrome_driver as driver:

        driver.maximize_window() 
        driver.get(url) # setting driver's url
        time.sleep(3) # waiting for page to load completely
        scroll_to_bottom(driver) # scrolling to bottom of page to capture all rows in table
        while(True):
          try: 
            table = driver.find_element(By.XPATH, "//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[2]/table/tbody") # scraping entire table
          except NoSuchElementException: 
            continue
          else: 
            break
        with open('table.txt', 'w') as table_file: # writing text contents of table to .txt file
            table_file.write(table.text)
        df = pandas.read_csv('table.txt', sep=" ", header=0) # loading .txt file as a data frame
        df.columns = ['Month', 'Day', 'Year', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume'] # adding column headers to data frame
        df.to_csv(os.path.join(directory, 'data', file)) # saving data frame to .csv with provided file name
        os.remove('table.txt') # removing .txt file

    driver.quit()
