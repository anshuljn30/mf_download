import pandas as pd
import cfscrape


def download():
    file_path = "C:\\Users\\Administrator\\Documents\\sd-src\\sql_data\\mutual_fund_data\\raw_info\\"
    url = "http://portal.amfiindia.com/DownloadSchemeData_Po.aspx?mf=0"
    scraper = cfscrape.create_scraper()

    cfurl = scraper.get(url)
    date = pd.to_datetime('today').strftime('%d-%b-%Y')
    save_file_name = "all_mf_info_" + date + '.xlsx'

    print('Downloading fund info file for ' + date)
    with open(file_path + save_file_name, 'wb') as f:
        f.write(cfurl.content)
