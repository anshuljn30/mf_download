from selenium import webdriver
from selenium.webdriver.support.ui import Select
import cfscrape
import time 
def download(dates):
	file_path = 'F:\\Projects\\internship\\test\\'
	chrome_driver = 'F:\\Projects\\internship\\birla_data\\chromedriver.exe'
	url = 'https://www.ltfs.com/companies/lnt-investment-management/downloads.html'

	scraper = cfscrape.create_scraper()
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.maximize_window()
	driver.get(url)

	for d in dates:
		year = d.strftime("%Y")
		month = d.strftime("%B")

		quarter = (d.month - 1)//3
		if quarter == 0:
			fiscal_year = str(d.year - 1) + '-' +d.strftime("%y")
		else:
			fiscal_year = d.strftime("%Y-") + str(int(d.strftime("%y")) + 1)	

		header = driver.find_element_by_xpath('.//h1[contains(text(), "Portfolio") and contains(text(), "Monthly")]')	
		header = header.find_element_by_xpath('.//parent::div')
		select_element = Select(header.find_element_by_xpath('.//descendant::select'))

		select_element.select_by_visible_text(fiscal_year)
		time.sleep(5)
		file = driver.find_elements_by_xpath('.//div[contains(text(), "' + year + '") and contains(text(), "' + month + '")  and contains(text(), "Equity")]')
		if file:
			file = file[0].find_element_by_xpath(".//parent::div")
			file = file.find_element_by_xpath(".//parent::div")
			file = file.find_elements_by_xpath(".//div/a")

			file_link = file[0].get_attribute("href")
			cfurl = scraper.get(file_link).content
			save_file_name = 'l&t_portfolios_' + d.strftime("%Y%m") + '.xls'

			with open(file_path + save_file_name, 'wb') as f:
				print('Downloading file for ' + year + month)
				f.write(cfurl)