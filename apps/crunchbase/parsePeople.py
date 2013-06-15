"""
First mine the people
"""
from crunchbase import Crunchbase
import os
from models.companyModels import *

c = Crunchbase(api_key=os.getenv("crunchbase_key"))
people_list = c.listPeople()
exceptions = []
for person in people_list:
	try:
		p = Person()
		p.crunchbase_url = "http://www.crunchbase.com/person/"+person['permalink']
		p.name = person['first_name'] + " " + person['last_name']
		person = c.getPersonData(person['permalink'])

		print person
		db.session.add(p)
		db.session.commit()
	except:
		print 'except'
		exceptions.append(person)

financial_org_list = c.listFinancialOrgs()
#print financial_org_list
infile = open("exceptions.txt", w)
print exceptions
infile.write(str(exceptions))
infile.close()
db.session.close()
