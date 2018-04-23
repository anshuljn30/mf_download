'''September 2013 is wrongly typed as Septempber 2013, so it refuses to download the file'''
from selenium import webdriver
import time
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'motilal')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%B')
        driver = webdriver.Chrome(executable_path=chrome_driver)
        driver.get("https://www.motilaloswalmf.com/downloads/mutual-fund/Month-End-Portfolio")
        file = driver.find_elements_by_xpath(
            './/td[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Month")]')

        while not file:
            driver.find_element_by_xpath('.//a[@class="select" and contains(text(), "Next")]').click()
            time.sleep(3)
            file = driver.find_elements_by_xpath(
                './/td[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Month")]')

        if file:
            file_link = file[0].find_element_by_xpath('.//parent::tr').find_element_by_xpath('.//a').get_attribute(
                "href")
            cfurl = scraper.get(file_link).content
            save_file_name = "motilal_portfolios_" + d.strftime('%Y%m') + '.xls'

            if cfurl != b'':
                print('Downloading file for ' + d.strftime('%b%Y'))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

            driver.close()
