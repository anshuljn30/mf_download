from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import cfscrape
import time

def download(dates, path):	
	file_path = os.path.join(path, 'hdfc') 
	if not os.path.exists(file_path):
		os.mkdir(file_path)
	chrome_driver = 'chromedriver.exe'
	
	scraper = cfscrape.create_scraper()

	url = 'http://www.hdfcfund.com/downloads/monthlyportfolio/c96fcab8-269f-4a81-8bfb-19b2cb9d120f'
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get(url)

	select_element = Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_DynamicTab_ddlYear"))
	select_element.select_by_visible_text("All")
	#wait for page to load
	time.sleep(10)
	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%b")	
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Portfolio")]')

		if file:
			for f in file:
				if ('FMP' not in f.get_attribute("text")) and ('Scheme' not in f.get_attribute("text")):
					file_link = f.get_attribute("href")
					break
			cfurl = scraper.get(file_link).content
			save_file_name = "hdfc_portfolios_" + d.strftime('%Y%m') + '.xls'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(os.path.join(file_path,save_file_name), 'wb') as f:
					f.write(cfurl)	

	driver.close()					