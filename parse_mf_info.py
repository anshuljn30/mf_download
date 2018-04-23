import pandas as pd
import numpy as np
import fuzzywuzzy.process as fwp


def parse_files(date):
    # Read all the master files
    root_path = "C:\\Users\\Administrator\\Documents\\sd-src\\sql_data\\"
    amc_master_file = root_path + "master_files\\new_amc_master.csv"
    fund_scheme_master_file = root_path + "master_files\\new_fund_scheme_master.csv"
    fund_master_file = root_path + "master_files\\new_fund_master.csv"
    xls_file_path = root_path + "mutual_fund_data\\raw_info\\"
    xls_out_path = root_path + "mutual_fund_data\\formatted_info\\"
    amc_master = pd.read_csv(amc_master_file)
    fund_scheme_master = pd.read_csv(fund_scheme_master_file, encoding='ISO-8859-1')
    fund_master = pd.read_csv(fund_master_file, encoding='ISO-8859-1')

    date = date.strftime('%d-%b-%Y')
    print('Parsing Fund Info data for ' + date + '....')
    xls_out_file = xls_out_path + "all_mf_info_" + date + '.csv'
    xls_file_name = 'all_mf_info_' + date
    xls_file = xls_file_path + xls_file_name + '.xlsx'

    df = pd.read_csv(xls_file, sep=',')
    df.index = range(len(df.index))

    # Remove any spaces from the fields
    df.replace('^\s+', '', regex=True, inplace=True)  # front
    df.replace('\s+$', '', regex=True, inplace=True)  # end
    df.columns = df.columns.str.replace('^\s+', '')  # front
    df.columns = df.columns.str.replace('\s+$', '')  # end

    # Scrape fund type and amc name and put them in separate column
    df.rename(columns={'AMC': 'amc_name', 'Code': 'scheme_code', 'Scheme Name': 'fund_name',
                       'Scheme Category': 'fund_category',
                       'Scheme NAV Name': 'scheme_name', 'Scheme Minimum Amount': 'min_amount',
                       'Launch Date': 'inception_date',
                       'Closure Date': 'closure_date', 'ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment': 'isin'},
              inplace=True)

    df_fund = df[['amc_name', 'fund_name', 'fund_category', 'inception_date', 'closure_date', 'min_amount']]
    df_fund = df_fund.drop_duplicates().reset_index(drop=True)

    # Merge amc_id from amc_master. If missing assign new ids
    fund_amc_temp = df_fund['amc_name'].drop_duplicates().reset_index(drop=True)
    fund_amc_temp['amc_name_closest'] = fund_amc_temp['amc_name'].apply(get_closest_match,
                                                                        args=(amc_master['amc_name'],))
    df_fund = pd.merge(df_fund, fund_amc_temp[['amc_name_closest', 'amc_name']], left_on='amc_name',
                       right_on='amc_name', how='left')
    # amc_master_temp = amc_master.replace({' mutual fund':''}, regex=True)
    df_fund = pd.merge(df_fund, amc_master[['amc_id', 'amc_name']], left_on='amc_name_closest',
                       right_on='amc_name', how='left')
    amc_master = assign_new_amc_ids(df_fund, amc_master, amc_master_file)
    df_fund = df_fund.drop('amc_id', axis=1)
    df_fund = pd.merge(df_fund, amc_master[['amc_id', 'amc_name']], left_on='amc_name',
                       right_on='amc_name', how='left')

    # Merge fund_id from fund_master. If missing assign new ids
    df_fund = pd.merge(df_fund, fund_master[['fund_id', 'fund_name']], left_on='fund_name',
                       right_on='fund_name', how='left')
    fund_master = assign_new_fund_ids(df_fund, fund_master, fund_master_file)

    # Fund scheme master
    df_scheme = df[['scheme_code', 'isin', 'scheme_name', 'fund_name']]
    df_scheme = pd.merge(df_scheme, fund_master[['fund_id', 'fund_name']], left_on='fund_name',
                         right_on='fund_name', how='left')
    d = difflib.Differ()
    df_scheme['chars'] = d.compare(df_scheme['scheme_name'], df_scheme['fund_name'])
    scheme_master = assign_new_scheme_ids(df_scheme, fund_scheme_master, fund_scheme_master_file)


def assign_new_amc_ids(df, amc_master, amc_master_file):
    df_amc = df[df['amc_id'].isnull()]
    nids = len(df_amc.index)
    if nids > 0:
        df_amc = df_amc.drop_duplicates(subset='amc_name').reset_index(drop=True)
        nids = len(df_amc.index)
        last_known_amc_id = amc_master['amc_id'].iloc[-1]
        df_amc['amc_id'] = pd.Series(
            range(last_known_amc_id + 1, last_known_amc_id + nids + 1, 1))
        df_amc = df_amc[['amc_id', 'amc_name']]
        print('Writing ', len(df_amc.index), ' new amcs to the amc_master...')
        with open(amc_master_file, 'a') as f:
            df_amc.to_csv(f, header=False, index=False)
        amc_master = amc_master.append(df_amc)
    return amc_master


def assign_new_fund_ids(df, fund_master, fund_master_file):
    df_fund = df[df['fund_id'].isnull()]
    nids = len(df_fund.index)
    if nids > 0:
        df_fund = df_fund.drop_duplicates(subset='fund_name').reset_index(drop=True)
        nids = len(df_fund.index)
        last_known_fund_id = fund_master['fund_id'].iloc[-1]
        df_fund['fund_id'] = pd.Series(
            range(last_known_fund_id + 1, last_known_fund_id + nids + 1, 1))
        df_fund = df_fund[
            ['fund_id', 'fund_name', 'amc_id', 'fund_category', 'inception_date', 'closure_date', 'min_amount']]
        print('Writing ', len(df_fund.index), ' new funds to the fund_master...')
        with open(fund_master_file, 'a') as f:
            df_fund.to_csv(f, header=False, index=False)
        fund_master = fund_master.append(df_fund)
    return fund_master


def assign_new_scheme_ids(df, fund_scheme_master, fund_scheme_master_file):
    df_scheme = df[df['scheme_id'].isnull()]
    nids = len(df_scheme.index)
    if nids > 0:
        df_scheme = df_scheme.drop_duplicates(subset='scheme_code').reset_index(drop=True)
        nids = len(df_scheme.index)
        last_known_scheme_id = fund_scheme_master['scheme_id'].iloc[-1]
        df_scheme['scheme_id'] = pd.Series(
            range(last_known_scheme_id + 1, last_known_scheme_id + nids + 1, 1))
        df_scheme = df_scheme[
            ['scheme_id', 'scheme_code', 'isin', 'scheme_name', 'fund_id', 'plan_type', 'distribution_option']]
        print('Writing ', len(df_scheme.index), ' new schemes to the fund_scheme_master...')
        with open(fund_scheme_master_file, 'a') as f:
            df_scheme.to_csv(f, header=False, index=False)
        fund_scheme_master = fund_scheme_master.append(df_scheme)
    return fund_scheme_master


def get_closest_match(row, master_list):
    min_score = 50
    match = fwp.extractOne(row, master_list)
    return match[0] if match[1] > min_score else None
