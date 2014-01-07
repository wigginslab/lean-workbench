import os
from flask import Flask, abort, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user
from flask_wtf.csrf import CsrfProtect
from apps.hypotheses.hypotheses_resource import Hypothesis_resource
from apps.facebook.facebook_resource import Facebook_resource
from apps.twitter.twitter_resource import Twitter_resource
from apps.wufoo.wufoo_resource import Wufoo_resource
from apps.google_analytics.google_analytics_resource import Google_analytics_resource

class SecuredStaticFlask(Flask):
    def send_static_file(self, filename):
    	protected_templates = ['partials/dashboard.html', 'partials/onboarding/stick.html']
    	print current_user.is_authenticated()
        # Get user from session
        if current_user.is_authenticated() or filename not in protected_templates:
            return super(SecuredStaticFlask, self).send_static_file(filename)
        else:
            return redirect('/static/partials/login.html')


app = SecuredStaticFlask(__name__,static_folder="static", static_path="/static")
#app = Flask(__name__)
CsrfProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = os.environ.get('secret_key')
app.config["DEBUG"] = True

# Setup Flask-Security users
app.config["SECURITY_PASSWORD_HASH"]="bcrypt"
app.config["SECURITY_EMAIL_SENDER"]="noreply@leanworkbench.com"
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = os.getenv("secret_key")
app.config["SECURITY_EMAIL_SENDER"] = "noreply@leanworkbench.com"
app.config["SECURITY_TRACKABLE"] = True
app.config["SECURITY_RECOVERABLE"] = True
app.config["SECURITY_REGISTER_URL"] = "/registration"


# Setup Flask-Security email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("email_username")
app.config['MAIL_PASSWORD'] = os.getenv("email_password")
app.config['SECURITY_EMAIL_SENDER'] = os.getenv("email_username")
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

#APIs
api = restful.Api(app)

api.add_resource(Hypothesis_resource, '/api/v1/hypotheses')
api.add_resource(Facebook_resource, '/api/v1/facebook')
api.add_resource(Twitter_resource, '/api/v1/twitter')
api.add_resource(Wufoo_resource, '/api/v1/wufoo')
api.add_resource(Google_analytics_resource, '/api/v1/ga')