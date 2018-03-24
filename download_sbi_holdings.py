from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time
import os
from shutil import copyfile

def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	default_download_path = 'C:\\Users\\Mreenav\\Downloads\\'
	scraper = cfscrape.create_scraper()

	url = 'https://www.sbimf.com/en-us/portfolios'
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get(url)	

	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")
		
		select_year = Select(driver.find_element_by_id("ddl_year"))
		select_year.select_by_visible_text(year)
		time.sleep(5)

		select_month = Select(driver.find_element_by_id("ddl_month"))
		select_month.select_by_visible_text(month)

		driver.find_element_by_id("ctl00_PlaceHolderMain_SBIMFControlSelectorID_ctl00_btnArchive").click()
		time.sleep(5)

		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '")  and contains(text(), "Equity")]')
		if not file:
			file = driver.find_elements_by_partial_link_text('equity')
		if file:
			file_link = file[0].get_attribute("href")
			driver.get(file_link)
			#set delay according to download speed
			time.sleep(60)
			print("Downloaded file for " + d.strftime("%B%Y"))
			for file in os.listdir(default_download_path):
				if ('.xls' in file) and (('equity' in file.lower()) or ('others' in file.lower())) and (year in file) and ((month.lower() in file.lower()) or (d.strftime("%m") in file.lower())):
					extension = file[file.index('.') : ]
					name = "sbi_portfolios_" + d.strftime('%Y%m') + extension
					copyfile(os.path.join(default_download_path, file), os.path.join(file_path, name))
					os.remove(os.path.join(default_download_path, file))
					#os.rename(os.path.join(file_path, file), os.path.join(file_path, name))		

	driver.close()				
