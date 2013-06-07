for company in companies:
	dump = json.dumps(company)
	investments = dump['investments'] # dictionary of investments

	investmentIds = storeInvestments(investments)



def storeInvestments(investments):
	for investment in investments:
		
