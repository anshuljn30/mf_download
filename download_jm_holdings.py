from selenium import webdriver
import cfscrape
import os
import pandas as pd


def download(dates, path):
    file_path = os.path.join(path, 'jm')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'
    scraper = cfscrape.create_scraper()

    url = 'http://www.jmfinancialmf.com/Downloads/FactSheets.aspx?SubReportID=A49C5853-C27A-42C5-9703-699AFEACE164'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(url)

    for d in dates:
        string = d.strftime("%m.%Y")
        if (d.year == 2017 and d.month > 8) or (d.year >= 2018):
            year = d.strftime("%Y")
            month = d.strftime("%B")
            file = file = driver.find_elements_by_xpath(
                './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Portfolio")]')
        else:
            file = driver.find_elements_by_xpath(
                './/a[contains(text(), "' + string + '") and contains(text(), "Portfolio")]')

        if file:
            for i in range(len(file)):
                file_link = file[i].get_attribute("href")
                cfurl = scraper.get(file_link).content
                save_file_name = d.strftime('%Y%m') + str(i) + '.xls'

                if cfurl != b'':
                    print('Downloading file for ' + d.strftime('%b%Y'))
                    with open(os.path.join(file_path, save_file_name), 'wb') as f:
                        f.write(cfurl)

            excel_files = []
            df_list = {}  # dictionary to store excel sheets as dataframes referenced by sheet names
            file_names = []  # file paths, to be deleted later
            for file in os.listdir(file_path):
                if (".xls" in file) and not (file.startswith('jm_portfolios_')):
                    excel_files.append(pd.ExcelFile(os.path.join(file_path, file)))
                    file_names.append(os.path.join(file_path, file))
            i = 0
            for file in excel_files:
                for sheet in file.sheet_names:
                    df_list[sheet + '_' + str(i)] = file.parse(sheet)
                i += 1

            writer = pd.ExcelWriter(os.path.join(file_path, 'jm_portfolios_' + d.strftime('%Y%m') + '.xls'))
            for sheet, data in df_list.items():
                data.to_excel(writer, sheet)
                writer.save()

            for file in file_names:
                os.remove(file)
    driver.close()
