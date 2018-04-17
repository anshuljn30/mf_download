from selenium import webdriver
import cfscrape
import time
import zipfile
import os

def download(dates, path):
	file_path = os.path.join(path, 'birla') 
	if not os.path.exists(file_path):
		os.mkdir(file_path)
	
	chrome_driver = 'chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%b")
		
		driver.get('https://mf.adityabirlacapital.com/Pages/Individual/Forms-Downloads/MonthlyPortfolio.aspx')
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Monthly Portfolios as on")]')

		while not file:
			try:
				driver.find_element_by_xpath('.//a[@class="goNext"]').click()
				time.sleep(3)
			except:
				break
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
				with open(os.path.join(file_path,save_file_name), 'wb') as f:
					f.write(cfurl)	

					
			
			current_file = zipfile.ZipFile(os.path.join(file_path,save_file_name))
			current_file.extractall(file_path)
			current_file.close()
			os.remove(os.path.join(file_path,save_file_name))
			for f in os.listdir(file_path):
				if '.xls' in f and not f.startswith('birla_portfolios_'):
					os.rename(os.path.join(file_path, f), os.path.join(file_path, 'birla_portfolios_' + d.strftime('%Y%m') + '.xls'))
	driver.close()		