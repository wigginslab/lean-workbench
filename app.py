import os
from flask import Flask, abort, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, current_user
from flask_wtf.csrf import CsrfProtect
from apps.hypotheses.hypothesis_resource import HypothesisResource
from apps.facebook.facebook_resource import FacebookResource
from apps.twitter.twitter_resource import TwitterResource
from apps.wufoo.wufoo_resource import WufooResource
from app.google_analytics.google_analytics_resource import GoogleAnalyticsResource

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

app = Flask(__name__)
CsrfProtect(app)
db = SQLAlchemy(app)

# Setup Flask-Security email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("email_username")
app.config['MAIL_PASSWORD'] = os.getenv("email_password")
app.config['SECURITY_EMAIL_SENDER'] = os.getenv("email_username")

#APIs
api = restful.Api(app)

api.add_resource(HypothesisResource, '/api/v1/hypotheses')
api.add_resource(FacebookResource, '/api/v1/facebook')
api.add_resource(TwitterResource, '/api/v1/twitter')
api.add_resource(WufooResource, 'api/v1/wufoo')
api.add_resource(GoogleAnalyticsResource, 'api/v1/ga')
