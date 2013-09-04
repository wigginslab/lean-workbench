import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
from flask.ext import restful
#from apps.googleanalytics.resources.google_analytics_resource import Google_Analytics_Resource
#from apps.hypotheses.hypotheses_resource import Hypothesis_Resource
from flask.ext.security import Security, SQLAlchemyUserDatastore 
from models.user import User, Role

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = os.environ.get('secret_key')
app.config["DEBUG"] = True

# Setup Flask-Security users
app.config["SECURITY_PASSWORD_HASH"]="bcrypt"
app.config["SECURITY_EMAIL_SENDER"]="noreply@leanworkbench.com"
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Setup Flask-Security email
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("email_username")
app.config['MAIL_PASSWORD'] = os.getenv("email_password")
mail = Mail(app)

#APIs
api = restful.Api(app)
#api.add_resource(Google_Analytics_Resource, '/api/v1/google-analytics/')
#api.add_resource(Hypothesis_Resource, '/api/v4/hypotheses/')
