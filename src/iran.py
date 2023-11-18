from persiantools.jdatetime import JalaliDate
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

cwd = os.getcwd()
directory = os.path.dirname(cwd)

def scrape_iran(file):
    def jalali_to_gregorian(jalali_dates):
        gregorian_dates = []
        for date in jalali_dates:
            year, month, day = map(int, date.split('/'))
            date = JalaliDate(year, month, day)
            gregorian_dates.append(date.to_gregorian())
        return gregorian_dates
  
    chrome_driver = webdriver.Chrome()
    with chrome_driver as driver:
        url = "https://tsetmc.com/IndexInfo/32097828799138957"
        driver.get(url)
        time.sleep(3)

        table = driver.find_element(By.XPATH, "//*[@id='MainContent']/div[5]/div[2]")
        driver.execute_script("arguments[0].scrollIntoView();", table)
        time.sleep(1)

        table.click()
        time.sleep(1)

        scroll = driver.find_element(By.XPATH, "//*[@id='MainContent']/div[5]/div[2]/div/div/div/div[1]/div[2]/div[3]")
        data = []
        while True:
            rows_xpath = "//*[@id='MainContent']/div[5]/div[2]/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div"
            rows = scroll.find_elements(By.XPATH, rows_xpath)
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//div[@role='gridcell']")
                row_data = [cell.text for cell in cells]
                if row_data not in data:
                    data.append(row_data)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 375;", scroll)
            time.sleep(1)
            if len(data) >= 100:
                break 
        df = pd.DataFrame(data, columns=['Date', 'Close', 'Low', 'High'])
        jalali_dates = df['Date'].tolist()
        gregorian_dates = jalali_to_gregorian(jalali_dates)
        df['Date'] = gregorian_dates
        df.to_csv(os.path.join(directory, 'data', file))

        driver.quit()
