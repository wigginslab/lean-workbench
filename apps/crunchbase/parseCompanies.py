"""
Script for mining crunchbase.
"""
from crunchbase import Crunchbase
from models.companyModels import *
import ast
import json

c = Crunchbase(os.getenv("crunchbase_key"))

companies= c.listCompanies()

for company in range(0, len(companies)):
	print companies[company]
#	investments = companies[company]['investments'] # dictionary of investments
#	print investments
#	company_name = dump['name']
#	tags = dump['tag_list']
#	store_investments(investments)
#	store_tags(tags)

def store_investments(investments):
	for investment in investments:
		pass		

def store__tags(tags):
	for tag in tags:
		pass
