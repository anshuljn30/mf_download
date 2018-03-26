from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time

def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	url = 'http://www.dhflpramericamf.com/statutory-disclosure/monthlyportfolio'
	
	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(chrome_driver)
	driver.get(url)

	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")
		select_element = Select(driver.find_element_by_id("C001_drp_MP"))
		select_element.select_by_visible_text("Monthly Portfolio " + year)
		time.sleep(10)
		file = driver.find_elements_by_xpath('.//a[contains(text(), "' + year + '") and contains(text(), "' + month + '") and contains(text(), "Portfolio")]')
		if file:
			file_link = file[0].get_attribute("href")

			cfurl = scraper.get(file_link).content
			save_file_name = 'dhfl_portfolios_' + d.strftime("%Y%m") + '.xls'

			with open(file_path + save_file_name, 'wb') as f:
				print('Downloading file for ' + year + month)
				f.write(cfurl)
	driver.close()			