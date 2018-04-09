from selenium import webdriver
import cfscrape
import time
import os

def download(dates, path):
    file_path = os.path.join(path, 'idbi') 
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.idbimutual.co.in/Downloads/Fund-Portfolios")
    driver.find_element_by_xpath(".//input[@name = 'ctl00$ctl00$ContentPlaceHolder1$chkclosepopup']").click()
    scraper = cfscrape.create_scraper()
    time.sleep(5)

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%b')

        driver.find_element_by_xpath("//select/option[@value='" + year + "']").click()
        time.sleep(5)

        portfolio_panel = driver.find_element_by_xpath("//td[contains(text(), '" + year + "') and contains(text(), '" + month + "')]")
        portfolio_panel = portfolio_panel.find_element_by_xpath('following-sibling::td')

        file = portfolio_panel.find_element_by_tag_name('a')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "idbi_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(os.path.join(file_path,save_file_name), 'wb') as f:
            f.write(cfurl.content)

    driver.close()
