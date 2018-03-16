from selenium import webdriver
import cfscrape


def download(dates):
    file_path = "C:\\Users\\Administrator\\Documents\\sd-src\\mutual_fund_data\\canara_robeco\\"
    chrome_driver = "C:\\Users\\Administrator\\Downloads\\chromedriver_win32\\chromedriver.exe"
    scraper = cfscrape.create_scraper()

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%b')
        driver = webdriver.Chrome(executable_path=chrome_driver)
        driver.get("http://www.canararobeco.com/forms-downloads/pages/Scheme-Monthly-Portfolio.aspx")
        file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Equity")]')

        while not file:
            driver.find_element_by_xpath('//td[@class="ms-paging"]/a/img[@alt="Next"]').click()
            file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Equity")]')

        if file:
            file_link = file[0].get_attribute('href')
            cfurl = scraper.get(file_link).content
            save_file_name = "canara_robeco_portfolios_" + d.strftime('%Y%m') + '.xlsx'

            if cfurl != b'':
                print('Downloading file for ' + d.strftime('%b%Y'))
                with open(file_path+save_file_name, 'wb') as f:
                    f.write(cfurl)

            driver.close()

