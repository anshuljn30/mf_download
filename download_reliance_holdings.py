from selenium import webdriver
import cfscrape

def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get('https://www.reliancemutual.com/investor-services/downloads/factsheets')
	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")

		file_block = driver.find_elements_by_xpath('.//label[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Monthly")]')
		
		if file_block:
			file =  file_block[0].find_element_by_xpath('.//parent::li')
			file_link = file.find_element_by_xpath('.//a').get_attribute("href")
			cfurl = scraper.get(file_link).content
			save_file_name = "reliance_portfolios_" + d.strftime('%Y%m') + '.xls'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(file_path+save_file_name, 'wb') as f:
					f.write(cfurl)
	
	driver.close()			