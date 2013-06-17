"""
First mine the people
"""
from crunchbase import Crunchbase
import os
from models.companyModels import *

class StorePeople:
	"""
	Store all people in the Crunchbase database
	"""
	def __init__():
		self.client = Crunchbase(api_key=os.getenv("crunchbase_key"))
		people_list = c.listPeople()
		exceptions = []
		for person in people_list:
			try:
				p = Person()
				person = c.getPersonData(person['permalink'])
				p.crunchbase_url = person['permalink']
				p.name = (person['first_name'] + " " + person['last_name']).encode('utf-8')

				print person
				db.session.add(p)
				db.session.commit()
			except:
				print 'except'
				exceptions.append(person)

		#print financial_org_list
		infile = open("exceptions.txt", w)
		print exceptions
		infile.write(str(exceptions))
		infile.close()
		db.session.close()
