from selenium import webdriver
import cfscrape
import time
import os


def download(dates, path):
    file_path = os.path.join(path, 'bnp_paribas')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    scraper = cfscrape.create_scraper()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    

    for d in dates:
        month = d.strftime('%b')
        year = d.strftime('%Y')
        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
        driver.get("https://www.bnpparibasmf.in/downloads/monthly-portfolio-scheme")

        disclaimer_panel = driver.find_element_by_xpath('.//a[@class = "greenButton download_close"]')
        disclaimer_panel.click()
        time.sleep(3)
        if month == 'Dec':
            year_to_click = str(int(year) + 1)
        else:
            year_to_click = year

        portfolio_panel = driver.find_element_by_xpath('.//div[@class = "dropdown"]')
        portfolio_panel.find_element_by_xpath('.//h3').click()
        time.sleep(1)
        year_panel = portfolio_panel.find_element_by_xpath('.//a[contains(text(), "' + year_to_click + '")]')
        year_panel.click()
        time.sleep(1)
        try:
            load_link = driver.find_element_by_xpath('.//a[text() = "Load more "]')
            load_link.click()
            time.sleep(2)
        except:
            pass

        try:
            load_link = driver.find_element_by_xpath('.//a[text() = "Load more "]')
            load_link.click()
            time.sleep(2)
        except:
            pass    

        file = driver.find_elements_by_xpath('.//p[(contains(text(), "Monthly Portfolio") or contains(text(), "MONTHLY PORTFOLIO")) and \
                                (contains(text(),"' + month + '") or contains(text(),"' + month.upper() + '")) and contains(text(),"' + year[2:4] + '")]')
        if file:
            file = file[0].find_element_by_xpath('../..')
            file_link = file.get_attribute('href')

            time.sleep(3)
            cfurl = scraper.get(file_link)
            save_file_name = "bnp_paribas_portfolios_" + d.strftime('%Y%m') + '.xls'

            print('Downloading file for Paribas on ' + d.strftime('%b%Y'))
            with open(os.path.join(file_path, save_file_name), 'wb') as f:
                f.write(cfurl.content)



        driver.close()
