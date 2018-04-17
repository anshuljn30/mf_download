from selenium import webdriver
import cfscrape
import os
import time
from shutil import copyfile, rmtree
import patoolib #pip install patoolib - required to extract .rar files

def download(dates, path):
	file_path = os.path.join(path, 'uti') 
	if not os.path.exists(file_path):
		os.mkdir(file_path)

	chrome_driver = 'chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get("https://www.utimf.com/forms-and-downloads/")

	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")

		block = driver.find_element_by_xpath('.//li[@id="consolidate-portfolio-disclosure"]')
		block.click()
		inputs = block.find_elements_by_xpath('.//input')
		inputs[0].click()
		time.sleep(3)
		inputs[0].find_element_by_xpath('..').find_element_by_xpath('.//li/span[contains(text(), "' + year + '")]').click()
		time.sleep(3)
		inputs = block.find_elements_by_xpath('.//input')
		inputs[1].click()
		time.sleep(3)
		inputs[1].find_element_by_xpath('..').find_element_by_xpath('.//li/span[contains(text(), "' + month + '")]').click()
		time.sleep(3)
		driver.find_element_by_xpath('.//div[@id="js-consolidate-portfolio-disclosure-submit"]').click()
		time.sleep(5)

		file = block.find_elements_by_xpath('.//a')

		if file:
			file_link = file[0].get_attribute("href")
			cfurl = scraper.get(file_link).content
			save_file_name = "uti_portfolios_" + d.strftime('%Y%m') + '.zip'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(os.path.join(file_path,save_file_name), 'wb') as f:
					f.write(cfurl)

			for f in os.listdir(file_path):
				if f.endswith(".zip") or f.endswith(".rar"):
					patoolib.extract_archive(os.path.join(file_path,f), outdir=file_path)
					os.remove(os.path.join(file_path,f))
			#sometimes archives are present inside archives therefore extract again		
			for f in os.listdir(file_path):
				if f.endswith(".zip") or f.endswith(".rar"):
					patoolib.extract_archive(os.path.join(file_path,f), outdir=file_path)
					os.remove(os.path.join(file_path,f))				
			for f in os.listdir(file_path):
				if f.startswith("pf") or f.startswith("sebi"):
					os.rename(os.path.join(file_path,f), "uti_portfolios_" + d.strftime('%Y%m') + ".xls")
			#sometimes there's a directory within the archive so need to check that as well	
			directories = next(os.walk(file_path))[1]
			for directory in directories:
				for f in os.listdir(os.path.join(file_path,directory)):
					if f.startswith("pf") or f.startswith("sebi"):
						copyfile(os.path.join(file_path,directory,f), os.path.join(file_path, "uti_portfolios_" + d.strftime('%Y%m') + ".xls") )
						rmtree(os.path.join(file_path,directory))

			#delete other files
			for f in os.listdir(file_path):
				if not f.startswith("uti_"):
					os.remove(os.path.join(file_path, f))
	driver.close()							