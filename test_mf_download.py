import pandas as pd
import download_all_mf_holdings as mf_holdings

dates = pd.date_range('20121031', '20180331', freq='m')
path = "C:\\Users\\surbh\\Documents\\India Asset Allocation\\mf_data\\holdings_raw"
mf_holdings.download(dates, path=path)
