"""
Script for mining crunchbase companies.
"""

from crunchbase import Crunchbase
from models.companyModels import *
import json

class StoreCrunchbase:
	"""
	Get a list of all the companies and people in the crunchbase database and store each one in our database
	"""

	def __init__(self):
		"""
		Gets all companies (startups and financial companies) and iterates through
		"""
		# get Crunchbase API client
		self.client = Crunchbase(os.getenv("crunchbase_key"))
		self.errors = []
		self.get_people()
		self.get_startups()
		self.get_financial_orgs()
		# open an error file to keep API errors in. Feel free to change this file.
		self.error_file = open("crunchbase_errors.log", "w")
		# track any errors parsing the API
		for error in self.errors:
			error_file.write(error)
		error_file.close()

	def store_tags(self,tags):
		tags_list = []
		for tag in tags:
			t = Tag(name=tag)
			db.session.add(t)
			db.session.commit()
			tags_list.append(t)	
		return tags_list

	def get_people(self):
		people_list = self.client.listPeople()
		for person in people_list:
			p = Person()
			person = self.client.getPersonData(person['permalink'])
			p.crunchbase_url = person['crunchbase_url']
			p.name = (person['first_name'] + " " + person['last_name']).encode('utf-8')
			p.born_year = person['born_year']
			p.born_month = person['born_month']
			p.born_day = person['born_day']
			db.session.add(p)
			db.session.commit()


	def get_startups(self):
		"""
		Gets all startups from the Crunchbase API and adds them to our database as Company models
		"""
		# get a list of all the "companies" from the Crunchbase API
		companies = self.client.listCompanies()
		self.save_companies(companies, "startup")

	def get_financial_orgs(self):
		"""
		Gets all financial organizations from the Crunchbase API and adds them to our database as Company models
		"""
		# get a list of all "financial organizations" from the Crunchbase API 
		financial_orgs = self.client.listFinancialOrgs()
		self.save_companies(financial_orgs, "financial organization")

	def save_companies(self, company_list, company_type):
		"""
		Saves companies (both startups and financial orgs) to database to company table

		args:
			company_list: a list of company dictionaries that have the company name as a key
			company_type: type of company
		"""
		company_logs = open("company.logs", "w")
		for company_index in range(0, len(company_list)):
			company_info= company_list[company_index]
			company_name = company_info['name']
			company = self.client.getCompanyData(company_name)
			if company != "error":
		
				
				# if resorted to searching CB for best match, you get a list back
				if company is list:
					# choose the first result
					print 'company is list'
					company_logs.write("company is list \n")
					company = company[0][0]
				
				# make roles

				company_logs.write("\n")
				company_logs.write(str(company))

				new_company = Company()
				if 'tag_list' in company.keys():
					if company['tag_list']:
						new_company.tags = self.store_tags(company['tag_list'])

				else:
					print 'fail whale'

				self.store_relationships(company['relationships'],company_name)
				new_company.number_of_employees = company['number_of_employees']
				new_company.founded_year = company['founded_year']
				new_company.founded_month = company['founded_month']
				new_company.founded_day = company['founded_day']
				new_company.type = company_type
				new_company.name = company_name
				new_company.crunchbase_url = company['crunchbase_url']
				new_company.homepage_url = company['homepage_url']
				print company
				if  company['image']:
					new_company.image = company['image']['available_sizes'][0][1]
				#add new company to database
				db.session.add(new_company)
				db.session.commit()
				db.session.close()

		# record error
		else:
			self.error_file.write(company_name)

	def store_relationships(self,relationships, company_name):
		"""
		TODO
		Store employees, their position, and whether or not they are still working for the company
		"""
		p = Person()

		print 'relationships'
		print relationships
		for person in relationships:
			print 'person'
			print person
			first_name = person['person']['first_name']
			last_name = person['person']['last_name']
			name = first_name + " " + last_name
			p_object = p.query.filter_by(name=name).first()
			print 'p_object'
			print p_object
			# if the person wasn't successfully mined previously
		  	if not p_object:
				self.errors.append(name)
			else:
				role = Role(role_name=person['title'], is_past=person['is_past'], company_name=company_name, person_id=p_object)
				db.session.add(p_object)
			db.session.commit()
			db.session.close()

	def store_funding(funding_rounds):
		"""
		TODO
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
				else:
					self.errors.append("Investor: "+investor.name +" not previously stored")
			new_round = InvestmentRound(
				round_code=investment['round_code'],
				 funded_day=investment['funded_day'],
				  funded_month=investment['funded_month'],
				   funded_year=investment['funded_year'],
				   investors = investors
			)
			db.session.add(new_round)
			db.session.commit()




StoreCrunchbase()
