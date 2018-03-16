from selenium import webdriver
import cfscrape
import time


def download(dates):
    file_path = "C:\\Users\\Administrator\\Documents\\sd-src\\mutual_fund_data\\idfc\\"
    chrome_driver = "C:\\Users\\Administrator\\Downloads\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.idfcmf.com/download-centre.aspx?tab=disclosures")
    scraper = cfscrape.create_scraper()
    driver.find_element_by_xpath("//span[contains(text(), 'Portfolios')]").click()
    time.sleep(5)

    for d in dates:
        date = d.strftime('%d-%m-%Y')

        file = driver.find_element_by_xpath('//a[contains(text(), "' + date + '")]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "idfc_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(file_path + save_file_name, 'wb') as f:
            f.write(cfurl.content)

    driver.close()
