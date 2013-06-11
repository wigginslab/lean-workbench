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
	error = False
	try:
		company = c.getCompanyData(company_name)
	except:
		errors.append[company]
		error = True
	if not error:
		if company is list:
			company = company[0]

		new_company = Company()
		# get people involved with company	
		new_company.relationships = store_relationships(company['relationships'])
		new_company.investors = store_investments(company)
		new_company.tags = store_tags(company)
		new_company.employees = store_employees(company)
		new_company.number_of_employees = company['number_of_employees']
		founded_year = company['founded_year']+company['founded_month']+company['founded_day']
		
		

	print errors
def store_investments(investments):
	for investment in investments:
		pass		

def store__tags(tags):
	for tag in tags:
		pass
