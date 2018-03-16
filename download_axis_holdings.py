from selenium import webdriver
import cfscrape


def download(dates):
    file_path = "C:\\Users\\Administrator\\Documents\\sd-src\\sql_data\\mutual_fund_data\\raw\\axis\\"
    chrome_driver = "C:\\Users\\Administrator\\Downloads\\chromedriver_win32\\chromedriver.exe"
    scraper = cfscrape.create_scraper()
    driver = webdriver.Chrome(executable_path=chrome_driver)

    driver.get("https://www.axismf.com/Downloads.aspx?Value=portfoliodetails")
    portfolio_panel = driver.find_element_by_xpath('.//span[text() = "Portfolio Details and Monthly disclosure of AAUM"]')
    portfolio_panel = portfolio_panel.find_element_by_xpath('../..')
    portfolio_panel = portfolio_panel.find_element_by_xpath('.//span[text() = "Portfolio Details"]')
    portfolio_panel = portfolio_panel.find_element_by_xpath('../..')

    for d in dates:
        year = d.strftime('%Y')
        month = d.strftime('%B')
        year_panel = portfolio_panel.find_element_by_xpath('.//span[text() = "' + year + '"]')
        year_panel = year_panel.find_element_by_xpath('../..')
        try:
            month_panel = year_panel.find_element_by_xpath('.//span[text() = "' + month + '"]')
            month_panel = month_panel.find_element_by_xpath('../..')
        except:
            month_panel = year_panel

        file = month_panel.find_element_by_xpath('.//a[contains(text(),"' + month + '")]')
        file_link = file.get_attribute('href')

        cfurl = scraper.get(file_link)
        save_file_name = "axis_portfolios_" + d.strftime('%Y%m') + '.xlsx'

        print('Downloading file for ' + d.strftime('%b%Y'))
        with open(file_path + save_file_name, 'wb') as f:
            f.write(cfurl.content)

    driver.close()

