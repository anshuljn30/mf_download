from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'dhfl_pramerica')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    chrome_driver = 'chromedriver.exe'
    url = 'http://www.dhflpramericamf.com/statutory-disclosure/monthlyportfolio'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(chrome_driver)
    driver.get(url)

    for d in dates:
        year = d.strftime("%Y")
        month = d.strftime("%B")
        select_element = Select(driver.find_element_by_id("C001_drp_MP"))
        select_element.select_by_visible_text("Monthly Portfolio " + year)
        time.sleep(10)
        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Portfolio")]')
        if file:
            file_link = file[0].get_attribute("href")

            cfurl = scraper.get(file_link).content
            save_file_name = 'dhfl_pramerica_portfolios_' + d.strftime("%Y%m") + '.xls'

            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                print('Downloading file for ' + year + month)
                f.write(cfurl)
    driver.close()
