import pandas as pd
import numpy as np


def parse_files(dates):
    # Read all the master files
    root_path = "C:\\Users\\Administrator\\Documents\\sd-src\\sql_data\\"
    amc_master_file = root_path + "master_files\\new_amc_master.csv"
    fund_scheme_master_file = root_path + "master_files\\new_fund_scheme_master.csv"
    xls_file_path = root_path + "mutual_fund_data\\raw_nav\\"
    xls_out_path = root_path + "mutual_fund_data\\formatted_nav\\"

    amc_master = pd.read_csv(amc_master_file)
    fund_scheme_master = pd.read_csv(fund_scheme_master_file, encoding='ISO-8859-1')

    for monthly_date in dates:
        print('Parsing NAV data for ' + monthly_date.strftime('%b %Y') + '....')

        daily_dates = pd.date_range(monthly_date + pd.offsets.MonthBegin(-1), monthly_date + pd.offsets.MonthEnd(0),
                                    freq='d')
        xls_out_file = xls_out_path + "all_mf_nav_" + monthly_date.strftime('%b_%Y') + '.csv'

        df_all_dates = pd.DataFrame()
        for date in daily_dates:
            date = date.strftime('%d-%b-%Y')
            xls_file_name = 'all_mf_nav_' + date
            xls_file = xls_file_path + xls_file_name + '.xlsx'

            try:
                df = pd.read_csv(xls_file, sep=';')

            except FileNotFoundError:
                print('No File found for date ' + date)
                continue

            df.index = range(len(df.index))
            # Remove any spaces from the fields
            df.replace('^\s+', '', regex=True, inplace=True)  # front
            df.replace('\s+$', '', regex=True, inplace=True)  # end

            # Scrape fund type and amc name and put them in separate column
            df.rename(columns={'Scheme Code': 'scheme_code', 'Scheme Name': 'scheme_name', 'Net Asset Value': 'nav',
                               'Repurchase Price': 'repurchase_price', 'Sale Price': 'sale_price', 'Date': 'date'},
                      inplace=True)
            where_desc = df['scheme_name'].isnull()
            scheme_code = df['scheme_code'].str.lower()
            where_amc_name = where_desc & scheme_code.isin(amc_master['amc_name'].str.lower())
            where_fund_type = where_desc & df['scheme_code'].notnull() & ~where_amc_name

            df_parsed = df
            df_temp = df['scheme_code']
            df_parsed['fund_type'] = df_temp[where_fund_type].reindex(df_temp.index, method='ffill')
            df_parsed['amc_name'] = df_temp[where_amc_name].reindex(df_temp.index, method='ffill')
            df_parsed = df_parsed[~where_fund_type & ~where_amc_name]
            df_parsed.replace('N.A.', np.NaN)
            df_parsed = df_parsed.drop_duplicates().reset_index(drop=True)
            df_parsed['amc_name'] = df_parsed['amc_name'].str.lower()
            df_parsed['scheme_code'] = pd.to_numeric(df_parsed['scheme_code'])

            # Combine all the files together
            if df_parsed.empty:
                print('Nothing Found!')
            else:
                df_all_dates = pd.concat([df_all_dates, df_parsed], ignore_index=True)
            del df, df_parsed

        print('Success!')
        # Merge amc_id from amc_master
        df_clean = pd.merge(df_all_dates, amc_master[['amc_id', 'amc_name']], left_on='amc_name',
                            right_on='amc_name', how='left')
        amc_master = assign_new_amc_ids(df_clean, amc_master, amc_master_file)

        # Merge new amc_ids into df_clean
        df_clean = df_clean.drop('amc_id', axis=1)
        df_clean = pd.merge(df_clean, amc_master[['amc_id', 'amc_name']], left_on='amc_name',
                            right_on='amc_name', how='left')

        # Merge scheme_id from fund_scheme_master
        df_clean = pd.merge(df_clean, fund_scheme_master[['scheme_code', 'scheme_id']], left_on='scheme_code',
                            right_on='scheme_code', how='left')
        fund_scheme_master = assign_new_scheme_ids(df_clean, fund_scheme_master, fund_scheme_master_file)

        # Merge new ids into df_clean
        df_clean = df_clean.drop('scheme_id', axis=1)
        df_clean = pd.merge(df_clean, fund_scheme_master[['scheme_code', 'scheme_id']], left_on='scheme_code',
                            right_on='scheme_code', how='left')
        df_clean = df_clean[['date', 'scheme_id', 'nav', 'repurchase_price', 'sale_price']]

        # Writing this clean df to a formatted file
        with open(xls_out_file, 'a') as f:
            print('Writing NAV file for all dates in ' + monthly_date.strftime('%b %Y') + '...')
            df_clean.to_csv(f, header=True, index=False)


def assign_new_amc_ids(df, amc_master, amc_master_file):
    df_amc = df[df['amc_id'].isnull()]
    nids = len(df_amc.index)
    if nids > 0:
        df_amc = df_amc.drop_duplicates(subset='amc_name').reset_index(drop=True)
        nids = len(df_amc.index)
        last_known_amc_id = amc_master['amc_id'].iloc[-1]
        df_amc['scheme_id'] = pd.Series(
            range(last_known_amc_id + 1, last_known_amc_id + nids + 1, 1))
        df_amc = df_amc[['amc_id', 'amc_name']]
        print('Writing ', len(df_amc.index), ' new amcs to the amc_master...')
        with open(amc_master_file, 'a') as f:
            df_amc.to_csv(f, header=False, index=False)
        amc_master = amc_master.append(df_amc)
    return amc_master


def assign_new_scheme_ids(df, fund_scheme_master, fund_scheme_master_file):
    df_scheme = df[df['scheme_id'].isnull()]
    nids = len(df_scheme.index)
    if nids > 0:
        df_scheme = df_scheme.drop_duplicates(subset='scheme_code').reset_index(drop=True)
        nids = len(df_scheme.index)
        last_known_scheme_id = fund_scheme_master['scheme_id'].iloc[-1]
        df_scheme['scheme_id'] = pd.Series(
            range(last_known_scheme_id + 1, last_known_scheme_id + nids + 1, 1))
        df_scheme = df_scheme[['scheme_id', 'scheme_code', 'scheme_name', 'amc_id', 'fund_type']]
        print('Writing ', len(df_scheme.index), ' new schemes to the fund_scheme_master...')
        with open(fund_scheme_master_file, 'a') as f:
            df_scheme.to_csv(f, header=False, index=False)
        fund_scheme_master = fund_scheme_master.append(df_scheme)
    return fund_scheme_master
