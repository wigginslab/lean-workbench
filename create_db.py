from models.user import db as user_tables
from apps.crunchbase.scripts.models.companyModels import db as cb_tables
from apps.googleanalytics.models.google_analytics_models import db as ga_tables
from apps.angellist.models.angellist_models import db as al_tables
from apps.hypotheses.hypotheses_model import db as h_tables
from apps.wufoo.wufoo_model import db as wf_tables 
from apps.fnordmetric.fnord_model import db as fm_tables 
# create user table
user_tables.create_all()
# create crunchbase tables
cb_tables.create_all()
# create google analytics tables
ga_tables.create_all()
# create angellist tales
al_tables.create_all()
# create hypotheses tables
h_tables.create_all()
# create wufoo tables
wf_tables.create_all()
# create fnordtables
fm_tables.create_all()
