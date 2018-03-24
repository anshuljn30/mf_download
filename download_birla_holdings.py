from selenium import webdriver
import cfscrape
import time
import zipfile
import os

def rename(year, month, name, file_path):
	for file in os.listdir(file_path):
		if (".xls" in file) and (month in file) and (year in file):
			os.rename(file, name[0:-4] + '.xls')



def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	scraper = cfscrape.create_scraper()

	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%b")
		driver = webdriver.Chrome(executable_path = chrome_driver)
		driver.get('https://mf.adityabirlacapital.com/Pages/Individual/Forms-Downloads/MonthlyPortfolio.aspx')
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Monthly Portfolios as on")]')

		while not file:
			driver.find_element_by_css_selector('a.goNext').click()
			file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Monthly Portfolios as on")]')

		if file:
			if file[0].get_attribute("href").startswith("http"):
				file_link = file[0].get_attribute("href")
			else:	
				file_link = 'https://mf.adityabirlacapital.com'+ file[0].get_attribute("onclick")[13:-16]
			cfurl = scraper.get(file_link).content
			save_file_name = "birla_portfolios_" + d.strftime('%Y%m') + '.zip'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(file_path+save_file_name, 'wb') as f:
					f.write(cfurl)	

			driver.close()		
			
			current_file = zipfile.ZipFile(file_path + save_file_name)
			current_file.extractall()
			current_file.close()
			os.remove(file_path + save_file_name)
			rename(year, month, save_file_name, file_path)