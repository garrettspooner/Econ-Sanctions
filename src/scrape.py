from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import yfinance as yf
import pandas
import time
import os

cwd = os.getcwd()
directory = os.path.dirname(cwd)
parent = os.path.join(directory, "chromedriver")
dict = {}

tickers = ["^GSPC", "^DJI", "^IXIC", "^NYA", "^XAX", "^BUK100P", "^RUT", "^VIX", "^FTSE", "^GDAXI", "^FCHI", "^STOXX50E", "^N100", "^BFX", "IMOEX.ME",
           "^N225", "HSI", "000001.SS", "399001.SZ", "^STI", "^AXJO", "^AORD", "^BSESN", "^JKSE", "^KLSE", "^NZ50", "^KS11", "^TWII", "^GSPTSE", "^BVSP",
           "^MXX", "^IPSA", "^MERV", "^TA125.TA", "^JN0U.JO"]

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
    
    # service = Service()
    # options = webdriver.ChromeOptions()
    # chrome_driver = webdriver.Chrome(service=service, options=options)
    
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



def query_yahoo():
  file_names = []
  for ticker in tickers:
      index = yf.Ticker(ticker) # getting ticker object
      df = index.history(period="max") # accessing historical data for given ticker
      if df.empty: # no data for this ticker
          continue
      else: # save historical data to .csv
          ticker = ticker.replace("^", "")
          file = f'ticker_{ticker}.csv'
          file_names.append(file)
          df.to_csv(os.path.join(directory, 'data', file))
  return file_names



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
