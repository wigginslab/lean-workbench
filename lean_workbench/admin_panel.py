from flask import Flask, send_file, make_response
from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from users.user_model import User, Role
from flask.ext.security import current_user

from database import db
import config

# write to CSV
from StringIO import StringIO
import csv
from flask.ext.admin.tools import rec_getattr


class MyView(ModelView):
	
    # Disable model creation
    can_create = False
    list_template = 'admin/list.html'
  	# Override displayed fields
    #column_list = ('login', 'email')
	def is_accessible(self):
		return False
		print current_user
		if 'admin' in [role.name for role in current_user.roles]:
		return True
		else:
		return False

    def _handle_view(self, name, *args, **kwargs):
    	if not self.is_accessible():
        	return abort(403)
    # Exporting
    def _get_data_for_export(self):
        view_args = self._get_list_extra_args()
 
        ## Map column index to column name
        #sort_column = self._get_column_by_idx(view_args.sort)
        #if sort_column is not None:
            #sort_column = sort_column[0]
 
        _, query = self.get_list(0, None, False, None, None, execute=False)
 
        return query.limit(None).all()
 
    def get_export_csv(self):
        self.export_columns = [column_name for column_name, _ in self._list_columns]
 
        io = StringIO()
        rows = csv.DictWriter(io, self.export_columns)
 
        data = self._get_data_for_export()
 
        rows.writeheader()
 
        for item in data:
            row = {column: unicode(rec_getattr(item, column)).encode('utf-8') for column in self.export_columns}
            rows.writerow(row)
 
        io.seek(0)
        return io.getvalue()
 	


    @expose('/export/')
    def export(self):
        response = make_response(self.get_export_csv())
        response.mimetype = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % self.name.lower().replace(' ', '_')
 
        return response

# init database
db.app = app
db.init_app(app)
app.config.from_object(config.Dev)
app.config.from_envvar("APP_CONFIG", silent=True) 
# Add administrative views here
admin = Admin(app)


admin.add_view(MyView(User, db.session))

app.run(debug=True)