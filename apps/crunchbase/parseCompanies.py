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
	try:
		company = c.getCompanyData(company_name)
	except:
		errors.append[company]
		
	if company is list:
			company = company[0]


		investors = store_investments(company)
		tags = store_tags(company)
		employees = store_employees(company)
		number_of_employees = company['number_of_employees']
		founded_year = company['founded_year']+company['founded_month']+company['founded_day']

		

	print errors
def store_investments(investments):
	for investment in investments:
		pass		

def store__tags(tags):
	for tag in tags:
		pass
