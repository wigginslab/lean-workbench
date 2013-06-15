"""
Script for mining crunchbase companies.
"""

from crunchbase import Crunchbase
from models.companyModels import *
import json

class storeCompanies():
	"""
	Get a list of all the companies in the crunchbase database and store each one in our database
	"""

	def __init__(self):
		"""
		Gets all companies and iterates through
		"""
		# get Crunchbase API client
		c = Crunchbase(os.getenv("crunchbase_key"))
		# get a list of all the companies in the Crunchbase API
		self.companies= c.listCompanies()
		# collect errors
		self.errors = []
		for company_index in range(0, len(self.companies)):
			company_dict = companies[company_index]
			self.company_name = company_dict['name']
			self.error = False
			try:
				company = c.getCompanyData(company_name)
			except:
				self.errors.append[company]
				error = True
			if not error:
				if company is list:
				company = company[0]
				new_company = Company()
	
			# company data storing functions
			new_company.relationships = self.store_relationships(company['relationships'])
			new_company.tags = self.store_tags(company)
			self.store_employees(company)
			new_company.number_of_employees = company['number_of_employees']
			new_company.founded_year = company['founded_year']+company['founded_month']+company['founded_day']

	print errors
	db.session.close()

	def store_relationships(relationships):
		"""
		Store employees, their position, and whether or not they are still working for the company
		"""
		p = Person()
		for person in relationships:
			first_name = person['first_name']
			last_name = person['last_name']
			name = first_name + " " + last_name
			p_object = p.query(name=name)
			# if the person wasn't successfully mined previously
		  if not p_object:
				errors.append(name)
			else:
				role = Role(role_name=person['title'], is_past=person['is_past'], company_name=self.company_name)
				p_object.roles + role
				db.session.add(p_object)
			db.session.commit()

	def store_funding(funding_rounds):
		"""
		Parse the fundraising information
		"""
		p = Person()
		for investment in funding_round['investments']:
			investors = []
			for investor in investment:
				# check investor is already in database as person
				investor = Person.query.filter_by(crunchbase_url=investor['permalink'])
			# if person already exists in the database
				if investor:
					investors.append(investor)
			new_round = InvestmentRound(round_code=investment['round_code'], funded_day=investment['funded_day'], funded_month=investment['funded_month'], funded_year=investment['funded_year'],investors = investors)
			db.session.add(new_round)
			db.session.commit()
			else:
				self.errors.append(investor)


	def store__tags(tags):
		tags_list = []
		for tag in tags:
			tags_list.append(tags)	
		return tags_list
