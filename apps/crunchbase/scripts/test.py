from crunchbase import Crunchbase
import os

c = Crunchbase(os.getenv("crunchbase_key"))
print c.getPersonData("david-miles")
