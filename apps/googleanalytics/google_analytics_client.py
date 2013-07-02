from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from models.google_analytics_model import *
from apiclient.discovery import build
from models.google_analytics_models import Google_Analytics_User_Model
import httplib2
from oauth2client.client import flow_from_clientsecrets, Credentials
import json
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')
app.debug = True

class Google_Analytics_API:

	def __init__(self, username):
		"""
		Creates a Google Analytics API object with a username based on stored credentials or by retrieving credentials via OAuth2 if user has not yet stored credentials or they have expired.

		args:
			username: username on the Lean Workbench sites
		"""
		self.credentials = Google_Analytics_User_Model.query.filter_by(username = username).first()
		if self.credentials:
			expires_on = self.credentials.as_dict()['token_expiry']
			current_time = datetime.now().isoformat()
			# if valid credentials are in the database
			print expires_on
			print current_time
			if expires_on > current_time:
				self.client = self.build_client(self.credentials)
		else:
			print "no credentials"
			return None

	def build_client(self, ga_user_credentials):
		credential_dict = ga_user_credentials.as_dict()
		credential_dict['_module'] = "oauth2client.client"
		credential_dict['_class'] = "OAuth2Credentials"
		credential_dict['token_uri'] = "https://accounts.google.com/o/oauth2/token"
		credential_dict['user_agent'] = "null"
		credential_dict['invalid'] = "false"
		credentials = Credentials.new_from_json(json.dumps(credential_dict))
		print credentials
		http = httplib2.Http()
		http = credentials.authorize(http)  
		#  Build the Analytics Service Object with the authorized http object
		client = build('analytics', 'v3', http=http)
		print client
		return client

	def step_one(self):
		"""
		Construct URL for user to login to Google through. 

		Returns:
			redirect url
		"""
		print 'step 1'
		google_analytics_callback_url = os.getenv("google_analytics_callback_url")
		google_analytics_client_id = os.getenv("google_analytics_client_id") 
		redirect_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/analytics.readonly&access_type=offline&redirect_uri="+google_analytics_callback_url+"&client_id="+google_analytics_client_id+"&hl=en&from_login=1&as=819ec18979456db&pli=1&authuser=0"
		return redirect_url

	def step_two(self,username, ga_api_code):
		"""
		Handle callback information
		"""
		print 'step 2'
		google_analytics_callback_url = os.getenv("google_analytics_callback_url")
		client_secrets = 'ga_client_secrets.json'
		flow = flow_from_clientsecrets(client_secrets,
						scope='https://www.googleapis.com/auth/analytics.readonly',
								message='%s is missing' % client_secrets, redirect_uri=google_analytics_callback_url)
		credentials = flow.step2_exchange(code=str(ga_api_code))
		credentials_json = json.loads(credentials.to_json())
		credentials_json['username'] = username
		http = httplib2.Http()
		http = credentials.authorize(http)  
		self.save_google_analytics_credentials(credentials_json)
		#  Build the Analytics Service Object with the authorized http object
		self.client = build('analytics', 'v3', http=http)
		return self.client

	def save_google_analytics_credentials(self,credentials_dict):
		"""
		Save Google Analytics Credentials to model
		"""
		print 'saving credentials'
		# store information necessary for building client
		GAUM = Google_Analytics_User_Model(credentials_dict)
		db.session.add(GAUM)
		db.session.commit()

	def get_user_accounts(self):
		accounts = self.client.management().accounts().list().execute()
		return accounts

