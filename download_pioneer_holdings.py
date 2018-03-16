from selenium import webdriver
import cfscrape
import time


def download(dates):
    file_path = "C:\\Users\\Administrator\\Documents\\sd-src\\mutual_fund_data\\baroda_pioneer\\"
    chrome_driver = "C:\\Users\\Administrator\\Downloads\\chromedriver_win32\\chromedriver.exe"
    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.barodapioneer.in/Downloads/Pages/Latest-Factsheet-and-Profile.aspx")

    for d in dates:
        year = d.strftime('%y')
        month = d.strftime('%b')

        portfolio_panel = driver.find_elements_by_xpath('.//div[contains(text(), "Portfolio")]')
        portfolio_panel = portfolio_panel[-1].find_element_by_xpath('following-sibling::div')

        trial_no = 1
        file = []
        while not file:
            if trial_no > 1:
                portfolio_panel.find_element_by_xpath('.//a/img[@alt="Next"]').click()
                portfolio_panel = driver.find_elements_by_xpath('.//div[contains(text(), "Portfolio")]')
                portfolio_panel = portfolio_panel[-1].find_element_by_xpath('following-sibling::div')

            file = portfolio_panel.find_elements_by_xpath(
                './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')
            trial_no = trial_no + 1

        if file:
            file_link = file[0].get_attribute('href')
            cfurl = scraper.get(file_link).content
            save_file_name = "baroda_pioneer_portfolios_" + d.strftime('%Y%m') + '.xlsx'

            if cfurl != b'':
                print('Downloading file for ' + d.strftime('%b%Y'))
                with open(file_path+save_file_name, 'wb') as f:
                    f.write(cfurl)

            driver.refresh()
            time.sleep(3)

