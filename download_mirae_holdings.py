from selenium import webdriver
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'mirae')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.miraeassetmf.co.in/downloads/download-archive/4")

    for d in dates:
        month = d.strftime('%B')
        year = d.strftime('%Y')

        portfolio_panel = driver.find_element_by_xpath('.//ul[@id="DownloadYears"]')

        year_to_click = int(year)
        if month == 'December':
            year_to_click = int(year) + 1

        if int(year_to_click) >= 2016:
            year_panel = portfolio_panel.find_element_by_xpath('.//a[contains(., "' + str(year_to_click) + '")]')
        else:
            year_panel = portfolio_panel.find_element_by_xpath('.//a[contains(., "Previous Years")]')

        link_name = year_panel.get_attribute('href')
        year_panel.click()
        tab_name = link_name[-5:]
        div_panel = driver.find_element_by_xpath('//div[@id="' + tab_name + '"]')

        file = []
        while not file:
            try:
                file = driver.find_element_by_xpath('//a[text() = "Portfolio Details - ' + month + ' ' + year + '"]')
            except:
                time.sleep(3)
                try:
                    div_panel.find_element_by_xpath('.//a[text()="Next"]').click()
                    time.sleep(3)
                except:
                    break
        if file:                

            file_link = file.get_attribute('href')

            cfurl = scraper.get(file_link)
            save_file_name = "mirae_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for Mirae on ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                f.write(cfurl.content)

        driver.refresh()
        time.sleep(3)
    driver.close()
