import os
from user_config import UserConfig

project_name="leanworkbench"


class Dev(UserConfig):
	DEBUG = True

	# Setup Flask-Security users
	SECURITY_PASSWORD_HASH = "bcrypt"
	SECURITY_EMAIL_SENDER = "noreply@leanworkbench.com"
	SECURITY_REGISTERABLE = True
	SECURITY_EMAIL_SENDER = "noreply@leanworkbench.com"
	SECURITY_TRACKABLE = True
	SECURITY_RECOVERABLE = True
	SECURITY_REGISTER_URL = "/registration"

	SQL_ALCHEMY_ECHO=False
	# Setup Flask-Security email
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	SECURITY_SEND_REGISTER_EMAIL = False

	QUICKBOOKS_OAUTH_CONSUMER_KEY="qyprdRIvDMh1GfAyToh39mK1WFlIDW"
	QUICKBOOKS_OAUTH_CONSUMER_SECRET="5FYBaYYwMJLNt7ZrQsvsCP1ZBgtAYRo0QJd7ea79"
	QUICKBOOKS_CALLBACK_URL="http://127.0.0.1:5000/connect/quickbooks/callback/"
	QUICKBOOKS_APP_TOKEN="e31e4187b9e5bb4bd2b94bdb9546dc76394a"
	BLUEPRINTS = [
	'google_analytics.app',
    'hypotheses.app',
    'twitter.app',
    'facebook.app',
    'quickbooks.app',
    'users.app'
        # or ('blog.views.app', {'url_prefix':'/blog'})
    ]  # each as (blueprint_instance, url_preffix)
  
	SQLALCHEMY_ECHO=True
	
class Testing(UserConfig):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/%s_test.sqlite" % project_name
    SQLALCHEMY_ECHO = False
