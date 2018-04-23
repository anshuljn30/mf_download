from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import cfscrape
import os


def download(dates, path):
    file_path = os.path.join(path, 'invesco')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'
    url = 'https://invescomutualfund.com/literature-and-form?tab=Complete'
    scraper = cfscrape.create_scraper()

    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)

    for d in dates:
        date_string = d.strftime("%m/%y")
        year = d.strftime("%Y")

        select_year = Select(driver.find_element_by_id('ddlYearCompleteMonthlyHoldings'))
        select_year.select_by_visible_text(year)
        time.sleep(5)

        files = driver.find_elements_by_xpath('.//a[contains(text(), "' + date_string + '")]')

        if files:
            for i in range(len(files)):
                file_link = files[i].get_attribute("href")
                file_name = d.strftime("%B%Y") + '_' + str(i) + '.xls'

                cfurl = scraper.get(file_link).content

                if cfurl != b'':
                    print('Downloading files for ' + d.strftime('%b%Y'))
                    with open(os.path.join(file_path, file_name), 'wb') as f:
                        f.write(cfurl)

            excel_files = []
            df_list = {}  # dictionary to store excel sheets as dataframes referenced by sheet names
            file_names = []  # file paths, to be deleted later
            for file in os.listdir(file_path):
                if (".xls" in file) and not (file.startswith('invesco_portfolios_')):
                    excel_files.append(pd.ExcelFile(os.path.join(file_path, file)))
                    file_names.append(os.path.join(file_path, file))
            i = 0
            for file in excel_files:
                for sheet in file.sheet_names:
                    df_list[sheet.replace(" ", "") + '_' + str(i)] = file.parse(sheet)
                i += 1

            writer = pd.ExcelWriter(os.path.join(file_path, 'invesco_portfolios_' + d.strftime('%Y%m') + '.xls'))
            for sheet, data in df_list.items():
                data.to_excel(writer, sheet)
                writer.save()

            for file in file_names:
                os.remove(file)

    driver.close()
