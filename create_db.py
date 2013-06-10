#from models.user import db 
from apps.crunchbase.models.companyModels import Person, Degree, InvestmentRound, Milestone, Tag, Role, db
db.create_all()

