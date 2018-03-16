import pandas as pd
import download_all_mf_nav as nav

dates = pd.date_range('20100101', '20171031', freq='d')
nav.download(dates)
