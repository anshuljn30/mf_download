import pandas as pd 
import numpy as np 
import os
from fuzzywuzzy import process
import difflib
import re
import warnings

warnings.filterwarnings("ignore")

def parse_files(date,root_path):    
    amc_master_file = os.path.join(root_path,"master_files","new_amc_master.csv")
    fund_scheme_master_file = os.path.join(root_path, "master_files", "new_fund_scheme_master.csv") #scheme nav
    fund_master_file = os.path.join(root_path,"master_files","new_fund_master.csv") #scheme
    xls_file_path = os.path.join(root_path, "mutual_fund_data", "raw_info")
    xls_out_path = os.path.join(root_path, "mutual_fund_data", "formatted_info")
    amc_master = pd.read_csv(amc_master_file)
    fund_scheme_master = pd.read_csv(fund_scheme_master_file, encoding='ISO-8859-1')
    fund_master = pd.read_csv(fund_master_file, encoding='ISO-8859-1')

    date = date.strftime('%d-%b-%Y')
    print('Parsing Fund Info data for ' + date + '....')
    xls_out_file = os.path.join(xls_out_path,"all_mf_info_" + date + '.csv')
    xls_file_name = 'all_mf_info_' + date
    xls_file = os.path.join(xls_file_path, xls_file_name + '.xlsx')

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
    '''///New'''
    fund_amc_temp = pd.DataFrame()
    fund_amc_temp['amc_name'] = df_fund['amc_name'].drop_duplicates().reset_index(drop=True)
    if len(amc_master.index) != 0:
        fund_amc_temp['amc_name_closest'] = fund_amc_temp['amc_name'].apply(get_closest_match,
                                                                            args=(amc_master['amc_name'],))
    else:
        fund_amc_temp['amc_name_closest'] = fund_amc_temp['amc_name']   
    df_fund = pd.merge(df_fund, fund_amc_temp[['amc_name_closest', 'amc_name']], left_on='amc_name',
                       right_on='amc_name', how='left')
     # amc_master_temp = amc_master.replace({' mutual fund':''}, regex=True)
    df_fund = pd.merge(df_fund, amc_master[['amc_id', 'amc_name']], left_on='amc_name_closest',
                       right_on='amc_name', how='left')
    df_fund.rename(columns = {'amc_name_x':'amc_name'}, inplace = True) ###
    amc_master = assign_new_amc_ids(df_fund, amc_master, amc_master_file)
    df_fund = df_fund.drop(['amc_id', 'amc_name_y'], axis=1)
    df_fund = pd.merge(df_fund, amc_master[['amc_id', 'amc_name']], left_on='amc_name',
                       right_on='amc_name', how='left')  
    df_fund['min_amount'] = df_fund['min_amount'].apply(extract_amount)                                                  
     # Merge fund_id from fund_master. If missing assign new ids
    df_fund = pd.merge(df_fund, fund_master[['fund_id', 'fund_name']], left_on='fund_name',
                       right_on='fund_name', how='left')

    df_fund["fund_category_new"], df_fund['fund_type'] = zip(*df_fund['fund_category'].apply(extract_fund_category))
    df_fund.loc[df_fund['fund_type'].isnull(), 'fund_type'] = df_fund[df_fund['fund_type'].isnull()]['fund_category'].apply(extract_fund_type)
    df_fund.loc[df_fund['fund_category_new'].isnull(), "fund_category_new"], _ = zip(*df_fund[df_fund['fund_category_new'].isnull()]["fund_name"].map(extract_fund_category_income_growth))
    df_fund['fund_type'] = df_fund['fund_category_new'].apply(extract_fund_type_from_category)
    df_fund.loc[df_fund['fund_type'].isnull(), "fund_type"] = df_fund[df_fund['fund_type'].isnull()]['fund_category'].apply(extract_fund_type)
    df_fund.loc[df_fund['fund_type'].isnull(), "fund_type"] = df_fund[df_fund['fund_type'].isnull()]['fund_name'].apply(extract_fund_type)
    df_fund.loc[df_fund['fund_category_new'].isnull(), 'fund_category_new'] = df_fund[df_fund['fund_category_new'].isnull()]['fund_category'].apply(fill_blank_fund_category)
    df_fund.loc[df_fund['fund_type'].isnull(), 'fund_type'] = df_fund[df_fund['fund_type'].isnull()]['fund_category'].apply(fill_blank_fund_type)

    fund_master = assign_new_fund_ids(df_fund, fund_master, fund_master_file)

    # Fund scheme master
    df_scheme = df[['scheme_code', 'isin', 'scheme_name', 'fund_name']]
    df_scheme['isin1'] = [""]*len(df_scheme.index)
    df_scheme['isin2'] = [""]*len(df_scheme.index)
    df_scheme['isin'].fillna(value = "", inplace = True)
    df_scheme['isin1'], df_scheme['isin2'] = zip(*df_scheme['isin'].map(clean_isin))
    df_scheme = df_scheme.drop(['isin'], axis = 1)
    df_scheme = pd.merge(df_scheme, fund_master[['fund_id', 'fund_name']], left_on='fund_name',
                         right_on='fund_name', how='left')

    df_scheme = pd.merge(df_scheme, fund_scheme_master[['scheme_id', 'scheme_name']], left_on='scheme_name',
                       right_on='scheme_name', how='left')
    #d = difflib.Differ() #import difflib?
    #df_scheme['chars'] = d.compare(df_scheme['scheme_name'], df_scheme['fund_name'])
    df_scheme['plan_type'] = df_scheme['scheme_name'].apply(extract_plan_type)
    #<temp>
    df_scheme['distribution_option'] = df_scheme['scheme_name'].apply(extract_distribution_option)
    df_scheme['distribution_option'].replace('^\s+', '', regex=True, inplace=True)  
    df_scheme['distribution_option'].replace('\s+$', '', regex=True, inplace=True)
    #</temp>
    df_scheme.loc[df_scheme['distribution_option'].notnull(), "distribution_option"] = df_scheme[df_scheme['distribution_option'].notnull()]['distribution_option'].apply(strip_extra)
    #df_scheme.to_csv("new_fund_scheme_master_temp.csv", index = False)
    fund_scheme_master = assign_new_scheme_ids(df_scheme, fund_scheme_master, fund_scheme_master_file)



def assign_new_amc_ids(df, amc_master, amc_master_file):
    df_amc = df[df['amc_id'].isnull()]
    nids = len(df_amc.index)
    if nids > 0:
        df_amc = df_amc.drop_duplicates(subset='amc_name').reset_index(drop=True)
        nids = len(df_amc.index)
        try:
            last_known_amc_id = amc_master['amc_id'].iloc[-1]
        except:
            last_known_amc_id = 0   
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
        try:
            last_known_fund_id = fund_master['fund_id'].iloc[-1]
        except:
            last_known_fund_id = 0    
        df_fund['fund_id'] = pd.Series(
            range(last_known_fund_id + 1, last_known_fund_id + nids + 1, 1))
        df_fund = df_fund[
            ['fund_id', 'fund_name', 'amc_id', 'fund_category', 'inception_date', 'closure_date', 'min_amount', 'fund_category_new', 'fund_type']]
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
        try:
            last_known_scheme_id = fund_scheme_master['scheme_id'].iloc[-1]
        except:
            last_known_scheme_id = 0    
        df_scheme['scheme_id'] = pd.Series(
            range(last_known_scheme_id + 1, last_known_scheme_id + nids + 1, 1))
        df_scheme = df_scheme[
            ['scheme_id', 'scheme_code', 'isin1', 'isin2', 'scheme_name', 'fund_id', 'plan_type', 'distribution_option']]
        print('Writing ', len(df_scheme.index), ' new schemes to the fund_scheme_master...')
        with open(fund_scheme_master_file, 'a') as f:
            df_scheme.to_csv(f, header=False, index=False)
        fund_scheme_master = fund_scheme_master.append(df_scheme)
    return fund_scheme_master


def get_closest_match(row, master_list):
    min_score = 50
    match = process.extractOne(row, master_list) #Process module not called earlier
    return match[0] if match[1] > min_score else None    

def extract_amount(row):
    numbers = re.findall( r'\d+\.*\d*', str(row))
    if numbers:
        return float(numbers[0])

def clean_isin(row):
    try:
        isin = re.findall('IN..........', str(row))
        if len(isin) == 2:
            return (str(isin[0]), str(isin[1]))
        elif len(isin) == 1:
            return (str(isin[0]), "")
        else:
            return ("", "")
    except:
        return ("", "")
           

def extract_plan_type(row):
    if "direct" in row.lower():
        return "Direct"
    elif "regular" in row.lower():
        return "Regular"       


def extract_distribution_option(row):
    string = row.split('-')
    for s in string:
        if ("growth" in s.lower()) or ("dividend" in s.lower()) or ("cumulative" in s.lower()) or ("div" in s.lower()) or ("bonus" in s.lower()):
                return s.upper()

def extract_fund_category(row):
    #debt
    if ("corporate" in row.lower()) or \
        ("long duration" in row.lower()) or ("medium duration" in row.lower()) or \
        ("medium" in row.lower()) or ("long" in row.lower()):
        return ("Income","Debt")
    elif ("gilt" in row.lower()) or ("government securities" in row.lower()) or ("money manager" in row.lower()) or \
    ("treasury" in row.lower()) or ("cd" in row.lower()) or ("cash" in row.lower()):
        return ("Gilt","Debt")
    elif ("liquid" in row.lower()) or ("money market" in row.lower()) or ("overnight" in row.lower()):
        return ("Liquid","Debt")
    elif ("short term" in row.lower()) or ("low duration" in row.lower()) or \
        ("short duration" in row.lower()) or ("ultra short duration" in row.lower()) or \
        ("banking" in row.lower()) or ("psu fund" in row.lower()):
        return ("Short Term","Debt")
    elif ("floating" in row.lower()) or ("floater" in row.lower()):
        return ("Floating","Debt")
    elif ("dynamic" in row.lower()):
        return ("Dynamic","Debt")
    elif ("credit risk" in row.lower()):
        return ("Credit Risk","Debt")
    elif ("fmp" in row.lower()) or ("fixed" in row.lower()) or ("days" in row.lower()) or ("months" in row.lower()) or \
    ("years" in row.lower()) or ("interval" in row.lower()):
        return ("FMP", "Debt")
    elif ("infrastructure debt" in row.lower()):
        return ("Infrastructure Debt", "Debt")
    #equity
    elif ("multi cap" in row.lower()) or ("large & mid" in row.lower()) or \
        ("dividend yield" in row.lower()) or ("focussed" in row.lower()) or ("contra" in row.lower()) or \
        ("multi" in row.lower()) or ("analyst" in row.lower()):
        return ("Multi Cap","Equity")
    elif ("large cap" in row.lower()) or ("top 100" in row.lower()) or ("blue chip" in row.lower()) or \
    ("bluechip" in row.lower()) or ("largecap" in row.lower()) or ("large-cap" in row.lower()):
        return ("Large Cap","Equity")
    elif ("mid cap" in row.lower()) or ("mid-cap" in row.lower()) or ("midcap" in row.lower()):
        return ("Mid Cap","Equity")
    elif ("small cap" in row.lower()) or ("smallcap" in row.lower()) or ("small-cap" in row.lower()) or \
    ("micro" in row.lower()) or ("junior cap" in row.lower()):
        return ("Small Cap","Equity")
    elif ("elss" in row.lower()):
        return ("ELSS","Equity")
    elif ("sectoral" in row.lower()) or ("pharma" in row.lower()) or ("infrastructure equity" in row.lower()) or \
    ("energy" in row.lower()) or ("resources" in row.lower()) or ("commodity" in row.lower()) or ("consumption" in row.lower()) \
    or ("manufacturing" in row.lower()) or ("infrastructure" in row.lower()):
        return ("Sectoral","Equity")
    elif ("value" in row.lower()) or ("pe ratio" in row.lower()):
        return ("Value","Equity")
    elif ("mnc" in row.lower()) or ("emerging" in row.lower()) or ("global" in row.lower()) or ("world" in row.lower()) or \
    ("japan" in row.lower()) or ("international" in row.lower()):
        return ("Others", "Equity")
    
    #hybrid
    elif ("balanced" in row.lower()) or ("balance") in row.lower():
        return ("Balanced", "Hybrid")
    elif ("aggressive" in row.lower()) or ("savings" in row.lower()):
        return ("Aggressive Hybrid", "Hybrid")
    elif ("conservative" in row.lower()) or ("mip" in row.lower()) or ("m i p" in row.lower()) or \
    ("mis" in row.lower()) or ("capital protection" in row.lower()) or ("multiple yield" in row.lower()) or \
    ("cpo" in row.lower()) or ("dual advantage" in row.lower()) or ("daf" in row.lower()):
        return ("Conservative Hybrid", "Hybrid")
    elif "arbitrage" in row.lower():
        return ("Arbitrage", "Hybrid")
    elif "asset allocation" in row.lower():
        return ("Asset Allocation", "Hybrid")
    elif "equity savings" in row.lower():
        return ("Equity Savings", "Hybrid")
       
    #other
    elif "gold etf" in row.lower():
        return ("Gold ETF","Other")
    elif "etf" in row.lower():
        return ("ETF","Other")
    elif "index" in row.lower():
        return ("Index Funds","Other")
    elif ("fof overseas" in row.lower()) or ("fund of funds overseas" in row.lower()) or ("fund of funds - overseas" in row.lower()) or \
    ("fof - overseas" in row.lower()):
        return ("FOF Overseas","Other")
    elif ("fof domestic" in row.lower()) or ("fund of funds domestic" in row.lower()) or ("fund of funds - domestic" in row.lower()) or \
    ("fof - domestic" in row.lower()):
        return ("FOF Domestic", "Other")
    elif ("children" in row.lower()) or ("child" in row.lower()):
        return ("Children's Fund","Other")
    elif "retirement" in row.lower():
        return ("Retirement Fund","Other")
    else:
        return (None,None )

def extract_fund_category_income_growth(row):
    #debt
    if ("income" in row.lower()) or ("corporate" in row.lower()) or \
        ("long duration" in row.lower()) or ("medium duration" in row.lower()) or \
        ("medium" in row.lower()) or ("long" in row.lower()):
        return ("Income","Debt") 
    elif ("corporate" in row.lower()) or \
        ("long duration" in row.lower()) or ("medium duration" in row.lower()) or \
        ("medium" in row.lower()) or ("long" in row.lower()):
        return ("Income","Debt")
    elif ("gilt" in row.lower()) or ("government securities" in row.lower()) or ("money manager" in row.lower()) or \
    ("treasury" in row.lower()) or ("cd" in row.lower()) or ("cash" in row.lower()):
        return ("Gilt","Debt")
    elif ("liquid" in row.lower()) or ("money market" in row.lower()) or ("overnight" in row.lower()):
        return ("Liquid","Debt")
    elif ("short term" in row.lower()) or ("low duration" in row.lower()) or \
        ("short duration" in row.lower()) or ("ultra short duration" in row.lower()) or \
        ("banking" in row.lower()) or ("psu fund" in row.lower()):
        return ("Short Term","Debt")
    elif ("floating" in row.lower()) or ("floater" in row.lower()):
        return ("Floating","Debt")
    elif ("dynamic" in row.lower()):
        return ("Dynamic","Debt")
    elif ("credit risk" in row.lower()):
        return ("Credit Risk","Debt")
    elif ("fmp" in row.lower()) or ("fixed" in row.lower()) or ("days" in row.lower()) or ("months" in row.lower()) or \
    ("years" in row.lower()) or ("interval" in row.lower()):
        return ("FMP", "Debt")
    elif ("infrastructure debt" in row.lower()):
        return ("Infrastructure Debt", "Debt")
    #equity
    elif ("multi cap" in row.lower()) or ("large & mid" in row.lower()) or \
        ("dividend yield" in row.lower()) or ("focussed" in row.lower()) or ("contra" in row.lower()) or \
        ("multi" in row.lower()) or ("analyst" in row.lower()):
        return ("Multi Cap","Equity")
    elif ("large cap" in row.lower()) or ("top 100" in row.lower()) or ("blue chip" in row.lower()) or \
    ("bluechip" in row.lower()) or ("largecap" in row.lower()) or ("large-cap" in row.lower()):
        return ("Large Cap","Equity")
    elif ("mid cap" in row.lower()) or ("mid-cap" in row.lower()) or ("midcap" in row.lower()):
        return ("Mid Cap","Equity")
    elif ("small cap" in row.lower()) or ("smallcap" in row.lower()) or ("small-cap" in row.lower()) or \
    ("micro" in row.lower()) or ("junior cap" in row.lower()):
        return ("Small Cap","Equity")
    elif ("elss" in row.lower()):
        return ("ELSS","Equity")
    elif ("sectoral" in row.lower()) or ("pharma" in row.lower()) or ("infrastructure equity" in row.lower()) or \
    ("energy" in row.lower()) or ("resources" in row.lower()) or ("commodity" in row.lower()) or ("consumption" in row.lower()) \
    or ("manufacturing" in row.lower()) or ("infrastructure" in row.lower()):
        return ("Sectoral","Equity")
    elif ("value" in row.lower()) or ("pe ratio" in row.lower()):
        return ("Value","Equity")
    elif ("mnc" in row.lower()) or ("emerging" in row.lower()) or ("global" in row.lower()) or ("world" in row.lower()) or \
    ("japan" in row.lower()) or ("international" in row.lower()):
        return ("Others", "Equity")
    elif ("growth" in row.lower()):
        return ("Growth", "Equity")
    
    #hybrid
    elif ("balanced" in row.lower()) or ("balance") in row.lower():
        return ("Balanced", "Hybrid")
    elif ("aggressive" in row.lower()) or ("savings" in row.lower()):
        return ("Aggressive Hybrid", "Hybrid")
    elif ("conservative" in row.lower()) or ("mip" in row.lower()) or ("m i p" in row.lower()) or \
    ("mis" in row.lower()) or ("capital protection" in row.lower()) or ("multiple yield" in row.lower()) or \
    ("cpo" in row.lower()) or ("dual advantage" in row.lower()) or ("daf" in row.lower()):
        return ("Conservative Hybrid", "Hybrid")
    elif "arbitrage" in row.lower():
        return ("Arbitrage", "Hybrid")
    elif "asset allocation" in row.lower():
        return ("Asset Allocation", "Hybrid")
    elif "equity savings" in row.lower():
        return ("Equity Savings", "Hybrid")
      
    #other
    elif "gold etf" in row.lower():
        return ("Gold ETF","Other")
    elif "etf" in row.lower():
        return ("ETF","Other")
    elif "index" in row.lower():
        return ("Index Funds","Other")
    elif ("fof overseas" in row.lower()) or ("fund of funds overseas" in row.lower()) or ("fund of funds - overseas" in row.lower()) or \
    ("fof - overseas" in row.lower()):
        return ("FOF Overseas","Other")
    elif ("fof domestic" in row.lower()) or ("fund of funds domestic" in row.lower()) or ("fund of funds - domestic" in row.lower()) or \
    ("fof - domestic" in row.lower()):
        return ("FOF Domestic", "Other")
    elif ("children" in row.lower()) or ("child" in row.lower()):
        return ("Children's Fund","Other")
    elif "retirement" in row.lower():
        return ("Retirement Fund","Other")
    else:
        return (None,None )

def extract_fund_type(row):
    if "hybrid" in row.lower():
        return "Hybrid"
    elif "debt" in row.lower():
        return "Debt"
    elif "equity" in row.lower():
        return "Equity"
    elif "other" in row.lower():
        return "Other"        

def extract_fund_type_from_category(row):
    if row == None:
        return None
    elif ("balanced" in row.lower()) or ("hybrid" in row.lower()) or ("arbitrage" in row.lower()) or ("asset allocation" in row.lower()) or \
    ("equity savings" in row.lower()):
        return "Hybrid"
    elif ("income" in row.lower()) or ("gilt" in row.lower()) or ("liquid" in row.lower()) or ("short term" in row.lower()) or \
    ("floating" in row.lower()) or ("dynamic" in row.lower()) or ("credit risk" in row.lower()) or ("fmp" in row.lower()) or \
    ("infrastructure debt" in row.lower()):
        return "Debt"
    elif ("cap" in row.lower()) or ("elss" in row.lower()) or ("sectoral" in row.lower()) or ("value" in row.lower()) or \
    ("others" in row.lower()) or ("growth" in row.lower()):
        return "Equity"
    elif ("etf" in row.lower()) or ("index" in row.lower()) or ("fof" in row.lower()) or ("children" in row.lower()) or \
    ("retirement" in row.lower()):
        return "Other"        

def fill_blank_fund_category(row):
    if row.lower() == "growth":
        return "Multi Cap"
    else:
        return "Income"
    
def fill_blank_fund_type(row):
    if row.lower() == "growth":
        return "Equity"
    else:
        return "Debt"        

def strip_extra(row):  
    if ("DIV" in row) or ("DIVIDEND" in row) or ("DIVIDED" in row):
        if ("QUARTERLY" in row) or ("QUATERLY" in row):
            return "Quarterly Dividend"
        elif "HALF YEARLY" in row:
            return "Half Yearly Dividend"
        elif ("ANNUAL" in row) or ("YEARLY" in row):
            return ("Annual Dividend")
        elif ("MONTHLY" in row):
            return "Monthly Dividend"
        elif ("DAILY" in row):
            return "Daily Dividend"
        elif ("WEEKLY" in row):
            return "Weekly Dividend"
        elif ("MATURITY" in row):
            return "Maturity Dividend"
        elif "PERIODIC" in row:
            return "Periodic Dividend"
        elif "FORTNIGHTLY" in row:
            return "Fortnightly Dividend"
        elif "REINVESTMENT" in row:
            return "Dividend Reinvestment"
        else:
            return "Dividend"
    elif "CUMULATIVE" in row:
        return "Cumulative Dividend"
    elif "GROWTH" in row:
        return "Growth"
    elif "BONUS" in row:
        if ("QUARTERLY" in row) or ("QUATERLY" in row):
            return "Quarterly Bonus"
        elif "HALF YEARLY" in row:
            return "Half Yearly Bonus"
        elif ("ANNUAL" in row) or ("YEARLY" in row):
            return ("Annual Bonus")
        elif ("MONTHLY" in row):
            return "Monthly Bonus"
        elif ("DAILY" in row):
            return "Daily Bonus"
        elif ("WEEKLY" in row):
            return "Weekly Bonus"
        else:
            return "Bonus"
        
    row = row.strip(" ")
    return row        