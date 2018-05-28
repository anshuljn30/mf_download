from selenium import webdriver
import cfscrape
import time
from selenium.webdriver.common.keys import Keys
import os


def download(dates, path):
    file_path = os.path.join(path, 'franklin_templeton')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.franklintempletonindia.com/investor/reports")

    #webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(10)
    dropdwn_panel = driver.find_element_by_xpath('.//span[contains(text(), "Disclosure of AUM by Geography")]')
    dropdwn_panel.click()
    time.sleep(2)
    dropdwn_panel = dropdwn_panel.find_element_by_xpath('../following-sibling::ul')
    dropdwn_panel = dropdwn_panel.find_element_by_xpath('.//li[@id = "MonthlyPortfolioDisclosure"]')
    dropdwn_panel.click()
    time.sleep(2)

    for d in dates:
        month = d.strftime('%b')
        year = d.strftime('%Y')

        file = driver.find_element_by_xpath('.//span[contains(text(), "ISIN Report") and \
                                contains(text(),"' + month + '") and contains(text(),"' + year + '")]')
        file = file.find_element_by_xpath('..')
        if file:
            file_link = file.get_attribute('href')

            cfurl = scraper.get(file_link)
            save_file_name = "franklin_templeton_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for Franklin Templeton on ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                f.write(cfurl.content)

    driver.close()
