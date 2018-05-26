from selenium import webdriver
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'sundaram')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get('https://www.sundarammutual.com/Monthly_Portfolio')

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%b')
        quarter = (d.month - 1) // 3
        if quarter == 0:
            fiscal_year = str(d.year - 1) + '-' + d.strftime("%Y")
        else:
            fiscal_year = d.strftime("%Y-") + str(int(d.strftime("%Y")) + 1)

        file_list = driver.find_elements_by_xpath('.//label[contains(text(), "' + fiscal_year + '")]/following::ul')

        if file_list:
            search_string = d.strftime("%b-%Y").upper()
            file = file_list[0].find_elements_by_xpath(
                './/a[contains(text(), "Equity") and contains(text(), "' + search_string + '")]')

            if file:
                file_link = file[0].get_attribute("href")
                cfurl = scraper.get(file_link).content
                save_file_name = "sundaram_portfolios_" + d.strftime('%Y%m') + '.xls'

                if cfurl != b'':
                    print('Downloading file for Sundaram on ' + d.strftime('%b%Y'))
                    with open(os.path.join(file_path, save_file_name), 'wb') as f:
                        f.write(cfurl)

    driver.close()
