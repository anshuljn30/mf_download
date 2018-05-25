from selenium import webdriver
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'principal')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.principalindia.com/downloads/disclosures.aspx")

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%B')

        p = driver.find_element_by_xpath('.//p[contains(text(), "Monthly Portfolios")]')
        div = p.find_element_by_xpath('.//following::div')
        file = div.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

        if file:
            file_link = file[0].get_attribute("href")
            cfurl = scraper.get(file_link).content
            save_file_name = "principal_portfolios_" + d.strftime('%Y%m') + '.xls'

            if cfurl != b'':
                print('Downloading file for Principal on ' + d.strftime('%b%Y'))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

    driver.close()
