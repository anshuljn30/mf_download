from selenium import webdriver
import cfscrape
import time
import os

def download(dates, path):
    file_path = os.path.join(path, 'indiabulls') 
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.indiabullsamc.com/portfolio-disclosure/")
    scraper = cfscrape.create_scraper()
    time.sleep(5)

    for d in dates:
        month = d.strftime('%b')
        year = d.strftime('%Y')

        file = driver.find_element_by_xpath('.//a[contains(., "' + month + '") and contains(., "' + year+ '")]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "indiabulls_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(os.path.join(file_path,save_file_name), 'wb') as f:
            f.write(cfurl.content)

    driver.close()
