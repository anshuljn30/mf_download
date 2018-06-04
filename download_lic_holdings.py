from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'lic')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    url = 'http://www.licmf.com/statuary_disclosure'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)

    for d in dates:
        year = d.strftime("%Y")
        month = d.strftime("%B")
        driver.get(url)
        portfolios = driver.find_element_by_xpath(
            './/h2[contains(text(), "Monthly") and contains(text(), "Portfolio")]')
        portfolios = portfolios.find_element_by_xpath('.//parent::div').click()
        time.sleep(3)

        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and (contains(text(), "Portfolio") or contains(text(), "portfolio"))]')

        if not file:
            quarter = (d.month - 1) // 3
            if quarter == 0:
                fiscal_year = str(d.year - 1) + '-' + d.strftime("%Y")
            else:
                fiscal_year = d.strftime("%Y-") + str(int(d.strftime("%Y")) + 1)
            driver.get('http://www.licmf.com/statuary_disclosure/archives')
            select_element = Select(driver.find_element_by_id("assesment_year"))
            select_element.select_by_visible_text(fiscal_year)
            time.sleep(5)

            portfolios = driver.find_element_by_xpath(
                './/h2[contains(text(), "Monthly") and contains(text(), "Portfolio")]')
            portfolios = portfolios.find_element_by_xpath('.//parent::div').click()
            time.sleep(3)

            file = driver.find_elements_by_xpath(
                './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and (contains(text(), "Portfolio") or contains(text(), "portfolio"))]')

        if file:
            file_link = file[0].get_attribute("href")
            cfurl = scraper.get(file_link, verify = False).content

            save_file_name = 'lic_portfolios_' + d.strftime("%Y%m") + '.xls'
            if cfurl != b'':
                print("Downloading file for LIC on" + d.strftime("%b%Y"))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

    driver.close()
