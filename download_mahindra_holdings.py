from selenium import webdriver
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'mahindra')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
    driver.get("http://www.mahindramutualfund.com/downloads#MANDATORY-DISCLOSURES")
    time.sleep(3)
    disclaimer_panel = driver.find_element_by_xpath('.//a[text()="I AM NOT A US PERSON/RESIDENT OF CANADA"]')
    disclaimer_panel.click()
    time.sleep(3)

    for d in dates:
        month = d.strftime('%B')
        year = d.strftime('%Y')

        portfolio_panel = driver.find_element_by_xpath('.//a[text()="Monthly Portfolio Disclosure"]')
        portfolio_panel.click()
        portfolio_panel = portfolio_panel.find_element_by_xpath('ancestor::h2/following-sibling::div')

        time.sleep(1)
        try:
            year_panel = portfolio_panel.find_element_by_link_text(year)
            year_panel.click()
        except:
            continue    

        time.sleep(1)
        file = driver.find_elements_by_xpath('//a[contains(text(), "Monthly Portfolio Disclosure") and contains(text(), \
                                            "' + month + '") and contains(text(), "' + year + '")]')
        if file:
            file_link = file[0].get_attribute('href')

            cfurl = scraper.get(file_link)
            save_file_name = "mahindra_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for Mahindra on ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                f.write(cfurl.content)

        driver.refresh()
        time.sleep(3)

    driver.close()
