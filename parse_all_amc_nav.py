import pandas as pd
from download_mf_data import parse_mf_nav as mf_nav

dates = pd.date_range('20100131', '20171231', freq='m')
mf_nav.parse_files(dates)
