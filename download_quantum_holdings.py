from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'quantum')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    url = 'https://www.quantumamc.com/schemeportfolio.aspx?SchemeId=0&FactSheetType=2'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)

    for d in dates:
        year = d.strftime("%Y")
        month = d.strftime("%B")

        select_scheme = Select(driver.find_elements_by_id("ddnScheme")[1])
        select_scheme.select_by_visible_text("Combined Portfolio")

        select_year = Select(driver.find_element_by_id("ddnYear"))
        select_year.select_by_visible_text(year)

        select_month = Select(driver.find_element_by_id("ddnMonth"))
        select_month.select_by_visible_text(month)

        driver.find_element_by_xpath('.//button[contains(text(), "Search")]').click()
        time.sleep(5)

        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

        if file:
            file_link = file[0].get_attribute("href")
            cfurl = scraper.get(file_link).content

            save_file_name = 'quantum_portfolios_' + d.strftime("%Y%m") + '.xls'
            if cfurl != b'':
                print("Downloading file for Quantum on " + d.strftime("%b%Y"))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)
    driver.close()
