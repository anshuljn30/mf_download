'''Certificate verification has to be disabled to download, because AdvisorKhoj is improperly
set up and throws a SSL Error (Bad Handshake, Certificate Verfication Failed)
'''
from selenium import webdriver
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'essel')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": file_path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)

    driver.get(
        'https://www.advisorkhoj.com/form-download-centre/Mutual-Funds/Essel-Mutual-Fund/Monthly-Portfolio-Disclosures')
    for d in dates:
        year = d.strftime("%Y")
        month = d.strftime("%B")

        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

        if file:
            file_link = file[1].get_attribute("href")
            print(file_link)
            cfurl = scraper.get(file_link, verify=False).content
            save_file_name = "essel_portfolios_" + d.strftime('%Y%m') + '.xls'

            if cfurl != b'':
                print('Downloading file for ' + d.strftime('%b%Y'))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

    driver.close()
