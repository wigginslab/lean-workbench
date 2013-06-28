from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from models.google_analytics_model import Google_Analytics_User_Model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')
app.debug = True

def save_google_analytics_credentials(credentials_dict):
	"""
	Save Google Analytics Credentials to model
	"""
	# store information necessary for building client
	print credentials_dict
	GAUM = Google_Analytics_User_Model(credentials_dict)

	print GAUM
	db.session.add(GAUM)
	db.session.commit()
