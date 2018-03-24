'''Certificate verification has to be disabled to download, because AdvisorKhoj is improperly
set up and throws a SSL Error (Bad Handshake, Certificate Verfication Failed)
'''
from selenium import webdriver
import cfscrape

def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get('https://www.advisorkhoj.com/form-download-centre/Mutual-Funds/Essel-Mutual-Fund/Monthly-Portfolio-Disclosures')
	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")
		
		
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

		if file:
			file_link = file[1].get_attribute("href")
			cfurl = scraper.get(file_link, verify = False).content
			save_file_name = "essel_portfolios_" + d.strftime('%Y%m') + '.xls'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(file_path+save_file_name, 'wb') as f:
					f.write(cfurl)	

	driver.close()		