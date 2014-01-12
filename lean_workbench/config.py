import os

project_name="leanworkbench"

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.getenv('db_url')
	SECRET_KEY = os.environ.get('secret_key')
	DEBUG = True

	# Setup Flask-Security users
	SECURITY_PASSWORD_HASH = "bcrypt"
	SECURITY_EMAIL_SENDER = "noreply@leanworkbench.com"
	SECURITY_REGISTERABLE = True
	SECURITY_PASSWORD_SALT = os.getenv("secret_key")
	SECURITY_EMAIL_SENDER = "noreply@leanworkbench.com"
	SECURITY_TRACKABLE = True
	SECURITY_RECOVERABLE = True
	SECURITY_REGISTER_URL = "/registration"


	# Setup Flask-Security email
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.getenv("email_username")
	MAIL_PASSWORD = os.getenv("email_password")
	SECURITY_EMAIL_SENDER = os.getenv("email_username")
	SECURITY_SEND_REGISTER_EMAIL = False

	BLUEPRINTS = [
	'google_analytics.app',
    'hypotheses.app'
        # or ('blog.views.app', {'url_prefix':'/blog'})
    ]  # each as (blueprint_instance, url_preffix)


class Dev(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class Testing(Config):
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/%s_test.sqlite" % project_name
    SQLALCHEMY_ECHO = False