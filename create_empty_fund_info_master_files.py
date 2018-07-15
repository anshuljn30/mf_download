import pandas as pd 
import os

def create_files(path):
	amc_master = pd.DataFrame({'amc_id':[], 'amc_name':[]}, columns = ['amc_id', 'amc_name'])
	amc_master.to_csv(os.path.join(path, "new_amc_master.csv"), index = False)

	fund_master = pd.DataFrame({'fund_id':[], 'fund_name':[], 'amc_id':[], 'fund_category':[], 'inception_date':[], 'closure_date':[], 'min_amount':[], 'fund_category_new':[], 'fund_type':[]}, columns = ['fund_id', 'fund_name', 'amc_id', 'fund_category', 'inception_date', 'closure_date', 'min_amount', 'fund_category_new', 'fund_type'])
	fund_master.to_csv(os.path.join(path, "new_fund_master.csv"), index = False)

	fund_scheme_master = pd.DataFrame({'scheme_id':[], 'scheme_code':[], 'isin1':[], 'isin2':[],  'scheme_name':[], 'fund_id':[], 'plan_type':[], 'distribution_option' : []}, columns = ['scheme_id', 'scheme_code', 'isin1', 'isin2', 'scheme_name', 'fund_id', 'plan_type', 'distribution_option'])
	fund_scheme_master.to_csv(os.path.join(path, "new_fund_scheme_master.csv"), index = False)