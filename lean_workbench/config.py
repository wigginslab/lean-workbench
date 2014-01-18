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

	SQLALCHEMY_DATABASE_URI='postgresql://neil:daemonlog1@localhost:5432/leanworkbench'
	SQL_ALCHEMY_ECHO=True
	# Setup Flask-Security email
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	SECURITY_SEND_REGISTER_EMAIL = False

	BLUEPRINTS = [
	'google_analytics.app',
    'hypotheses.app',
    'twitter.app',
    'facebook.app'
        # or ('blog.views.app', {'url_prefix':'/blog'})
    ]  # each as (blueprint_instance, url_preffix)
  
	SQLALCHEMY_ECHO=True
class Testing(UserConfig):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/%s_test.sqlite" % project_name
    SQLALCHEMY_ECHO = False
