from models.user import db as user_tables
from apps.crunchbase.scripts.models.companyModels import db as cb_tables
from apps.googleanalytics.models.google_analytics_models import db as ga_tables
from apps.angellist.models.angellist_models import db as al_tables
# create user table
user_tables.create_all()
# create crunchbase tables
cb_tables.create_all()
# create google analytics tables
ga_tables.create_all()
# create angellist tales
al_tables.create_all()

