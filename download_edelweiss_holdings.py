from selenium import webdriver
import cfscrape
import os

def download(dates, path):
    file_path = os.path.join(path, 'edelweiss') 
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://www.edelweissmf.com/StatutoryDisclosures/monthly-portfolio.aspx")
    scraper = cfscrape.create_scraper()

    for d in dates:
        year = d.strftime('%y')
        month = d.strftime('%b')
        year_pane = driver.find_elements_by_xpath('.//div[.//li[contains(text(), "' + year + '")]]')
        year_pane[-1].find_element_by_xpath('.//li[contains(text(), "' + year + '")]').click()
        month_pane = year_pane[-1].find_elements_by_xpath('.//div[.//div[.//li[contains(text(), "' + month + '")]] \
         and @class = "TabbedPanelsContent TabbedPanelsContentVisible"]')
        month_pane[-1].find_element_by_xpath('.//li[contains(text(), "' + month + '")]').click()

        file = driver.find_element_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "edelweiss_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(os.path.join(file_path,save_file_name), 'wb') as f:
            f.write(cfurl.content)

    driver.close()
