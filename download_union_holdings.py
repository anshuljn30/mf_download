from selenium import webdriver
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'union')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.unionmf.com/downloads/others/monthlyportfolios.aspx")

    year_panel = driver.find_element_by_xpath('.//span[contains(text(), "Select Year")]')
    year_panel = year_panel.find_element_by_xpath('following-sibling::div//select')

    for d in dates:
        month = d.strftime('%b')
        year = d.strftime('%Y')

        year_panel.find_element_by_xpath('./option[text() = "' + year + '"]').click()
        time.sleep(2)

        file = driver.find_element_by_xpath(
            './/a[contains(text(),"' + month + '") and contains(text(),"' + year + '")]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "union_portfolios_" + d.strftime('%Y%m') + '.xls'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(os.path.join(file_path, save_file_name), 'wb') as f:
            f.write(cfurl.content)
