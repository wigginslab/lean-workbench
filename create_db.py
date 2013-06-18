from models.user import db as user_db
from apps.crunchbase.scripts.models.companyModels import db as crunchbase_db

# create user table
user_db.create_all()
# create crunchbase tables
crunchbase_db.create_all()
