from datetime import datetime
from flask import Flask
from werkzeug import generate_password_hash, check_password_hash
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

class Google_Analytics_User_Model(db.Model):
	
	__tablename__ = "google_analytics_oauth_credentials"
	
	uid = db.Column(db.Integer, primary_key=True)
	token_expiry = db.Column(db.String)
	access_token = db.Column(db.String)
	client_id = db.Column(db.String)
	client_secret = db.Column(db.String)
	profile_id = db.Column(db.String)
	refresh_token = db.Column(db.String)
	revoke_uri = db.Column(db.String)
	id_token = db.Column(db.String)
	token_response = db.Column(db.String)
	username = db.Column(db.String)

	def __init__(self, credentials_dict):
		self.username = credentials_dict.get("username")
		self.access_token = credentials_dict.get("access_token")
		self.client_id = credentials_dict.get("client_id"),
		self.client_secret = credentials_dict.get("client_secret")
		self.refresh_token = credentials_dict.get("refresh_token")
		self.token_expiry = credentials_dict.get("token_expiry")
		self.token_uri = credentials_dict.get("token_uri")
		self.user_agent = credentials_dict.get("user_agent")

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}


