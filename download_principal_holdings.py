from selenium import webdriver
import cfscrape


def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path=chrome_driver)
	driver.get("http://www.principalindia.com/downloads/disclosures.aspx")


	for d in dates:
		year = d.strftime('%Y')
		month = d.strftime('%B')

		div = driver.find_element_by_xpath('.//div[@contentindex="25c"]')
		file = div.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '")]')

		if file:
			file_link = file[0].get_attribute("href")
			cfurl = scraper.get(file_link).content
			save_file_name = "principal_portfolios_" + d.strftime('%Y%m') + '.xls'

			if cfurl != b'':
				print('Downloading file for ' + d.strftime('%b%Y'))
				with open(file_path+save_file_name, 'wb') as f:
					f.write(cfurl)	

	driver.close()		
