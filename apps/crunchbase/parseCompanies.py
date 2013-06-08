
from Crunchbase import Crunchbase
c = Crunchbase(os.getenv("crunchbase_key"))
#return jsonify(c.listCompanies)
companies = c.listCompanies()

for company in companies:
	dump = json.dumps(company)
	investments = dump['investments'] # dictionary of investments
	company_name = dump['name']
	tags = dump['tag_list']
	store_investments(investments)
	store_tags(tags)



def store_investments(investments):
	for investment in investments:
		

def store__tags(tags):
	for tag in tags: