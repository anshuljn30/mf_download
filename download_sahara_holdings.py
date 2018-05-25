from selenium import webdriver
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'sahara')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.saharamutual.com/Downloads/MonthlyPortfolio.aspx")
    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%B')

        file = driver.find_elements_by_xpath(
            './/div[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')
        '''if not file:
            driver.find_element_by_xpath('.//a[contains(text(),"Archive")]').click()
            file = driver.find_elements_by_xpath('.//div[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')
        '''
        if file:
            file_link = file[0].find_element_by_xpath('.//following::a[contains(text(), "Equity")]').get_attribute(
                "href")
            cfurl = scraper.get(file_link).content
            save_file_name = "sahara_portfolios_" + d.strftime('%Y%m') + '.xls'

            if cfurl != b'':
                print('Downloading file for Sahara on ' + d.strftime('%b%Y'))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

    driver.close()
