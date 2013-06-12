from crunchbase import Crunchbase
import os
from models.companyModels import *

c = Crunchbase(api_key=os.getenv("crunchbase_key"))
people_list = c.listPeople()
for person in people_list:
	p = Person()
	print person
	p.crunchbase_url = "http://www.crunchbase.com/person/"+person['permalink']
	p.name = person['first_name'] + " " + person['last_name']
	person = c.getPersonData(person['permalink'])
	print  ' -----'
	
	print person
	db.session.add(p)
	db.session.commit()

financial_org_list = c.listFinancialOrgs()
#print financial_org_list

db.session.close()
