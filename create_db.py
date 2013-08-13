from models.user import db as user_tables, API 
from apps.crunchbase.scripts.models.companyModels import db as cb_tables
from apps.googleanalytics.models.google_analytics_models import db as ga_tables
from apps.angellist.models.angellist_models import db as al_tables
from apps.wufoo.wufoo_models import db as wf_tables
from apps.hypotheses.hypotheses_model import db as h_tables
from apps.wufoo.wufoo_model import db as wf_tables 
from apps.fnordmetric.fnord_model import db as fm_tables 
from apps.crunchbase.models.crunchbase_model import db as cb_model_table
from run import db

# create user table
user_tables.create_all()
# create crunchbase tables
cb_tables.create_all()
# create google analytics tables
ga_tables.create_all()
# create angellist tables
al_tables.create_all()
# create wufoo tables
wf_tables.create_all()
# create hypotheses tables
h_tables.create_all()
# create wufoo tables
wf_tables.create_all()
# create fnordtables
fm_tables.create_all()
# crunchbase user model table
cb_model_table.create_all()
