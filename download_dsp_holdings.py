'''Note: 1. Data for August 2014, July 2014, May 2014, April 2014 are missing.
 All data from February 2014 and earlier are missing as well.
 2. Using cfscrape creates a corrupted file of size (4-8kB).
 3. Script attempts to download like a regular user, copies the files to file_path and then renames all the files in one go.
 4. Usage is similar to all other scripts. Pass a list of datetime objects to download.
 5. Zip File consists of two files - open ended holdings and close ended holdings. These files are combined.
'''
from selenium import webdriver
import cfscrape
import os
from shutil import copyfile, rmtree
import time
import zipfile
import pandas as pd


def rename(file_path, date):
    file_types = ['open', 'close']
    excel_files = []
    df_list = {}  # dictionary to store excel sheets as dataframes referenced by sheet names
    file_names = []  # file paths, to be deleted later
    for file in os.listdir(file_path):
        if '.xls' in file and not file.startswith('dsp_blackrock_'):
            if file == 'Matured_Factsheet Closed Ended Sept 14.xls':
                continue
            for file_type in file_types:
                if file_type in file.lower():
                    excel_files.append(pd.ExcelFile(os.path.join(file_path, file)))
                    file_names.append(os.path.join(file_path, file))

    for file in excel_files:
        for sheet in file.sheet_names:
            df_list[sheet] = file.parse(sheet)

    # for files inside directories
    directories = next(os.walk(file_path))[1]
    for directory in directories:
        for file in os.listdir(os.path.join(file_path, directory)):
            if (".xls" in file):
                for file_type in file_types:
                    if file_type in file.lower():
                        excel_files.append(pd.ExcelFile(os.path.join(file_path, directory, file)))
        for file in excel_files:
            for sheet in file.sheet_names:
                df_list[sheet] = file.parse(sheet)
        rmtree(os.path.join(file_path, directory))  # delete directory

    writer = pd.ExcelWriter(os.path.join(file_path, 'dsp_portfolios_' + date.strftime('%Y%m') + '.xls'))
    for sheet, data in df_list.items():
        data.to_excel(writer, sheet)
    writer.save()

    for file in file_names:
        os.remove(file)


def download(dates, path):
    file_path = os.path.join(path, 'dsp')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": file_path}
    chrome_options.add_experimental_option("prefs", prefs)

    for d in dates:
        year = d.strftime("%Y")
        month = d.strftime("%b")

        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        driver.get('https://dspblackrock.com/about-us/mandatory-disclosure/month-end-portfolio-disclosures')
        time.sleep(5)
        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Portfolio")]')

        if file:
            driver.get(file[0].get_attribute("href"))
            print('Downloading file for ' + d.strftime('%b%Y'))
            # set delay as per maximum expected time to download a 500KB file
            time.sleep(20)
            # Copy files from default download address to path
            for file in os.listdir(file_path):
                if file.startswith("month_end_portfolio"):
                    source = os.path.join(file_path, file)
                    current_file = zipfile.ZipFile(source)
                    current_file.extractall(file_path)
                    current_file.close()
                    os.remove(source)
            driver.close()
            try:
                rename(file_path, d)
            except:
                continue
