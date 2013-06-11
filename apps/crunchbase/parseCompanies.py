"""
Script for mining crunchbase.
"""
from crunchbase import Crunchbase
from models.companyModels import *
import ast
import json

c = Crunchbase(os.getenv("crunchbase_key"))

companies= c.listCompanies()

errors = []
for company_index in range(0, len(companies)):
	company_dict = companies[company_index]
	company_name = company_dict['name']
	company = c.getCompanyData(company_name)
	try:
		if company is list:
			pass
		else:
			pass
	except:
		errors.append[company]
	print errors
def store_investments(investments):
	for investment in investments:
		pass		

def store__tags(tags):
	for tag in tags:
		pass
