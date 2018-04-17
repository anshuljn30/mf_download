from selenium import webdriver
import cfscrape
import time
import os

def download(dates, path):
    file_path = os.path.join(path, 'idfc') 
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.idfcmf.com/download-centre.aspx?tab=disclosures")
    scraper = cfscrape.create_scraper()
    driver.find_element_by_xpath("//span[contains(text(), 'Portfolios')]").click()
    time.sleep(5)

    for d in dates:
        date = d.strftime('-%m-%Y')

        file = driver.find_elements_by_xpath('//a[contains(text(), "' + date + '")]')
        if file:
            file_link = file[0].get_attribute('href')

            cfurl = scraper.get(file_link)
            save_file_name = "idfc_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path,save_file_name), 'wb') as f:
                f.write(cfurl.content)

    driver.close()
