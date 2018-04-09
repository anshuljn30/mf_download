import time
from selenium import webdriver
import cfscrape
import os

def download(dates, path):
    file_path = os.path.join(path, 'escorts') 
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.escortsmutual.com/downloads.aspx?Cat=Portfolio")
    scraper = cfscrape.create_scraper()

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%B')

        driver.find_element_by_xpath("//select[@name='drpyear']/option[text()='" + year + "']").click()
        driver.find_element_by_xpath("//select[@name='drpmonth']/option[text()='" + month + "']").click()
        driver.find_element_by_xpath("//input[@src='Images/gp.gif']").click()
        time.sleep(5)

        file = driver.find_element_by_xpath('.//a[contains(text(), "Portfolio") and @class = "dnlink"]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "escorts_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(os.path.join(file_path,save_file_name), 'wb') as f:
            f.write(cfurl.content)

    driver.close()
