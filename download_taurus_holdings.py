from selenium import webdriver
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'taurus')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.taurusmutualfund.com/Download/portfolio.php")

    for d in dates:
        month = d.strftime('%B')
        year = d.strftime('%Y')

        file = driver.find_elements_by_xpath('.//a[contains(text(), "Monthly Scheme Portfolio") and \
                                contains(text(),"' + month + '") and contains(text(),"' + year + '")]')
        if file:
            file_link = file[0].get_attribute('href')

            cfurl = scraper.get(file_link)
            save_file_name = "taurus_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for Taurus on ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                f.write(cfurl.content)

    driver.close()
