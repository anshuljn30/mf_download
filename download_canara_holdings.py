from selenium import webdriver
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'canara_robeco')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    chrome_driver = "chromedriver.exe"
    scraper = cfscrape.create_scraper()

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%b')
        driver = webdriver.Chrome(executable_path=chrome_driver)
        driver.get("http://www.canararobeco.com/forms-downloads/pages/Scheme-Monthly-Portfolio.aspx")
        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Equity")]')

        while not file:
            try:
                driver.find_element_by_xpath('//td[@class="ms-paging"]/a/img[@alt="Next"]').click()
            except:
                break
            file = driver.find_elements_by_xpath(
                './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Equity")]')

        if file:
            file_link = file[0].get_attribute('href')
            cfurl = scraper.get(file_link).content
            save_file_name = "canara_robeco_portfolios_" + d.strftime('%Y%m') + '.xls'

            if cfurl != b'':
                print('Downloading file for Canara Robeco' + d.strftime('%b%Y'))
                with open(os.path.join(file_path, save_file_name), 'wb') as f:
                    f.write(cfurl)

            driver.close()
