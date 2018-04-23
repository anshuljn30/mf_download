from selenium import webdriver
import time
import os


def download(dates, path):
    url = 'https://assetmanagement.kotak.com/portfolios'
    file_path = os.path.join(path, 'kotak')
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    chrome_driver = 'chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": file_path}
    chrome_options.add_experimental_option("prefs", prefs)

    for d in dates:

        driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        driver.get(url)
        year = d.strftime("%Y")
        month = d.strftime("%B")

        file = driver.find_elements_by_xpath(
            './/a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

        if file:
            file_link = file[0].get_attribute("href")
            driver.get(file_link)

            save_file_name = 'kotak_portfolios_' + d.strftime("%Y%m") + '.xls'
            print("Downloading file for" + d.strftime("%b%Y"))
            time.sleep(30)  # set as per connection speed
            for f in os.listdir(file_path):
                if '.xls' in f:
                    if not f.startswith("kotak_"):
                        os.rename(os.path.join(file_path, f), os.path.join(file_path, save_file_name))
            driver.close()
