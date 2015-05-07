from flask import Flask, send_file, make_response
from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from users.user_model import User, Role
from quickbooks.quickbooks_model import QuickbooksDailyAccountBalance
from flask.ext.security import current_user

from database import db
import config

# write to CSV
from StringIO import StringIO
import csv
from flask.ext.admin.tools import rec_getattr


class QuickbooksView(ModelView):
	
    list_template = 'admin/list.html'


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

    def is_accessible(self):
   		return 'admin' in [role.name for role in current_user.roles]
class UserView(ModelView):
	
    list_template = 'admin/list.html'
  	# Override displayed fields
    column_list = ('id', 'email', 'company', 'last_login_at', 
    	'current_login_at','login_count','active','onboarded')


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

    def is_accessible(self):
   		return 'admin' in [role.name for role in current_user.roles]

from flask import Flask, render_template, redirect, url_for, current_app
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user, auth_token_required, current_user
from users.user_model import User, Role
from database import db
from flask_wtf.csrf import CsrfProtect
import os
from werkzeug import SharedDataMiddleware
from flask.ext import restful
from hypotheses.hypotheses_resource import HypothesisResource
from quickbooks.quickbooks_resource import Quickbooks_resource
from facebook.facebook_resource import FacebookResource
from twitter.twitter_resource import TwitterResource
from wufoo.wufoo_resource import WufooResource
from forms.registration_form import ExtendedRegisterForm
from google_analytics.google_analytics_resource import GoogleAnalyticsResource
from ghosting.ghosting_resource import Ghosting_resource
from scale.scale_resource import Scale_resource
from users.user_resource import UserResource
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.admin import Admin


class SecuredStaticFlask(Flask):
	def send_static_file(self, filename):
		protected_templates = ['partials/dashboard2.html', 'partials/onboarding/stick.html', 'partials/onboarding/scale.html','partials/onboarding/virality.html', 'partials/measurements.html', 'partials/measurements2.html', 'partials/onboarding/wufoo.html', 'partials/onboarding/pay.html', 'partials/scale.html', 'partials/onboarding/welcome.html', 'partials/dashboard/optimization.html','partials/dashboard/baseline.html''partials/dashboard/operations.html', 'partials/dashboard/done.html']
		# Get user from session
		if not current_user.is_anonymous() or filename not in protected_templates:
			return super(SecuredStaticFlask, self).send_static_file(filename)
		else:
			return redirect('/static/partials/signin.html')


def __import_blueprint(blueprint_str):
	split = blueprint_str.split('.')
	module_path = '.'.join(split[0: len(split) - 1])
	variable_name = split[-1]
	mod = __import__(module_path, fromlist=[variable_name])
	return getattr(mod, variable_name)


def config_str_to_obj(cfg):
	if isinstance(cfg, basestring):
		module = __import__('config', fromlist=[cfg])
		return getattr(module, cfg)
	return cfg

def app_factory(config, app_name=None, blueprints=None):
	app_name = app_name or __name__
	app = SecuredStaticFlask(app_name, static_url_path='/static')
	config = config_str_to_obj(config)
	configure_app(app, config)
	configure_blueprints(app, blueprints or config.BLUEPRINTS)
	configure_error_handlers(app)
	configure_database(app)
	configure_context_processors(app)
	configure_template_filters(app)
	configure_extensions(app)
	configure_before_request(app)
	configure_views(app)
	return app

def configure_app(app, config):
	app.config.from_object(config)
	app.config.from_envvar("APP_CONFIG", silent=True)  # avaiable in the server


def configure_blueprints(app, blueprints):
	for blueprint_config in blueprints:
		blueprint = None
		kw = {}

		if (isinstance(blueprint_config, basestring)):
			blueprint = blueprint_config
		elif (isinstance(blueprint_config, dict)):
			blueprint = blueprint_config[0]
			kw = blueprint_config[1]

		blueprint = __import_blueprint(blueprint)
		app.register_blueprint(blueprint, **kw)


def configure_error_handlers(app):

	@app.errorhandler(403)
	def forbidden_page(error):
		"""
		The server understood the request, but is refusing to fulfill it.
		Authorization will not help and the request SHOULD NOT be repeated.
		If the request method was not HEAD and the server wishes to make public
		why the request has not been fulfilled, it SHOULD describe the reason for
		the refusal in the entity. If the server does not wish to make this
		information available to the client, the status code 404 (Not Found)
		can be used instead.
		"""
		return render_template("access_forbidden.html"), 403


	@app.errorhandler(404)
	def page_not_found(error):
		"""
		The server has not found anything matching the Request-URI. No indication
		is given of whether the condition is temporary or permanent. The 410 (Gone)
		status code SHOULD be used if the server knows, through some internally
		configurable mechanism, that an old resource is permanently unavailable
		and has no forwarding address. This status code is commonly used when the
		server does not wish to reveal exactly why the request has been refused,
		or when no other response is applicable.
		"""
		return render_template("page_not_found.html"), 404


	@app.errorhandler(405)
	def method_not_allowed_page(error):
		"""
		The method specified in the Request-Line is not allowed for the resource
		identified by the Request-URI. The response MUST include an Allow header
		containing a list of valid methods for the requested resource.
		"""
		return render_template("method_not_allowed.html"), 405


	@app.errorhandler(500)
	def server_error_page(error):
		return render_template("server_error.html"), 500


def configure_database(app):
	"Database configuration should be set here"
	# uncomment for sqlalchemy support
	from database import db
	db.app = app
	db.init_app(app)


def configure_context_processors(app):
	"Modify templates context here"
	pass


def configure_template_filters(app):
	"Configure filters and tags for jinja"
	pass


def configure_extensions(app):
	"Configure extensions like mail and login here"
	pass


def configure_before_request(app):
	pass


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def configure_views(app):
	
	user_datastore = SQLAlchemyUserDatastore(db, User, Role)
	security = Security(app, user_datastore, confirm_register_form= ExtendedRegisterForm)
	csrf = CsrfProtect(app)
	migrate = Migrate(app, db)
	admin = Admin(app, name="Lean Workbench Admin")


	admin.add_view(UserView(User, db.session))
	admin.add_view(QuickbooksView(QuickbooksDailyAccountBalance, db.session))



	print current_user
	@app.route('/')
	def index():
		if current_user.is_authenticated():
			logged_in = True
			return redirect(url_for('dashboard'))
		else:
			logged_in=False
			return render_template('public.html', logged_in=logged_in)

	@app.route('/signin', methods=["POST", "GET"])
	@app.route('/signup', methods=["POST", "GET"])
	def sign():
		if current_user.is_authenticated():
			return redirect(url_for('dashboard'))
		return render_template('public.html', logged_in=False)

	@auth_token_required
	@app.route('/stats', methods=['POST','GET'])
	@app.route('/stats/1',methods=['POST','GET'])
	@app.route('/onboarding/stick', methods=['POST', 'GET'])
	@app.route('/onboarding/scale', methods=['POST', 'GET'])
	@app.route('/onboarding/virality', methods=['POST','GET'])
	@app.route('/onboarding/pay', methods=['POST','GET'])
	@app.route('/onboarding/empathy', methods=['POST','GET'])
	@app.route('/export', methods=['POST','GET'])
	@app.route('/scale', methods=['POST', 'GET'])    
	@app.route('/results', methods=['POST', 'GET'])  
	@app.route('/privacy', methods=['POST','GET'])
	@app.route('/eula', methods=['POST','GET'])
        @app.route('/optimization', methods=['POST','GET'])
        @app.route('/baseline', methods=['POST','GET'])
        @app.route('/operations', methods=['POST','GET'])
        @app.route('/onboarding/done', methods=['GET','POST'])
	@app.route('/dashboard', methods=['POST', 'GET'])    
	def dashboard():
		"""
		"""
		if not current_user.is_authenticated():
			return render_template('public.html', logged_in=False)
                else:
			return render_template('public.html', logged_in=True)
		
	@app.route('/welcome', methods=['POST','GET'])
	def welcome():
		current_user.onboarded = True
                db.session.add(current_user)
                db.session.commit()
		return render_template('public.html', logged_in=True)

	api = restful.Api(app, decorators=[csrf.exempt])
	api.add_resource(HypothesisResource, '/api/v1/hypotheses')
	api.add_resource(FacebookResource, '/api/v1/facebook')
	api.add_resource(TwitterResource, '/api/v1/twitter')
	api.add_resource(WufooResource, '/api/v1/wufoo')
	api.add_resource(GoogleAnalyticsResource, '/api/v1/google-analytics')
	api.add_resource(Quickbooks_resource, '/api/v1/quickbooks')
	api.add_resource(UserResource, '/api/v1/users')
	api.add_resource(Ghosting_resource, '/api/v1/ghosting')
	api.add_resource(Scale_resource, '/api/v1/scale')
