'''Data missing from january 2013 and earlier '''
from selenium import webdriver
import cfscrape
import time
import zipfile
import os
from shutil import rmtree
import pandas as pd

def rename(date, file_path):
	file_types = ['Arbitrage', 'CPOF', 'Debt', 'Equity', 'FMP', 'FOF', 'Gold', 'Hybrid', 'Interval', 'MYF']
	excel_files = []
	df_list = {}
	file_names = []
	for file in os.listdir(file_path):
		if (".xls" in file) and not (file.startswith('icici')):
			for file_type in file_types:
				if file_type in file:
					excel_files.append(pd.ExcelFile(os.path.join(file_path,file)))
					file_names.append(os.path.join(file_path,file))
	for file in excel_files:
		for sheet in file.sheet_names:
			df_list[sheet] = file.parse(sheet)


	directories = next(os.walk(file_path))[1]
	for directory in directories:
		for file in os.listdir(os.path.join(file_path,directory)):
			if (".xls" in file):
				for file_type in file_types:
					if file_type in file:
						excel_files.append(pd.ExcelFile(os.path.join(file_path,directory,file)))	
		for file in excel_files:
			for sheet in file.sheet_names:
				df_list[sheet] = file.parse(sheet)
					
		rmtree(os.path.join(file_path, directory))	

	writer = pd.ExcelWriter(os.path.join(file_path, 'icici_portfolios_' + date.strftime('%Y%m') + '.xls'))
	for sheet, data in df_list.items():
		data.to_excel(writer, sheet)
	writer.save()
	
	for file in file_names:
		os.remove(file)			


def download(dates, path):
	file_path = os.path.join(path, 'icici') 
	if not os.path.exists(file_path):
		os.mkdir(file_path)

	chrome_driver = 'chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get('https://www.icicipruamc.com/Downloads/MonthlyPortfolioDisclosure.aspx')
	
	for d in dates:
		year = d.strftime("%y")
		month = d.strftime("%b")
		
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Monthly Portfolio")]')


		if file:
			file_link = file[0].get_attribute("href")
			cfurl = scraper.get(file_link).content
			save_file_name = "icici_portfolios_" + d.strftime('%Y%m') + '.zip'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(os.path.join(file_path,save_file_name), 'wb') as f:
					f.write(cfurl)

			try:
				current_file = zipfile.ZipFile(os.path.join(file_path,save_file_name))
				current_file.extractall(file_path)
				current_file.close()
				os.remove(os.path.join(file_path,save_file_name))
				rename(d, file_path)
			except:
				print("Could not unzip " + save_file_name)		


	driver.close()		
			
			