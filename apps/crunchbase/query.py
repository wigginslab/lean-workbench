from crunchbase import Crunchbase
import os 


infile = open("companies.json", "w'")

c = Crunchbase(os.getenv("crunchbase_key"))
infile.write(str(c.listCompanies()))