import urllib
import urllib2
import os
from apiclient.discovery import build
from google_analytics_models import Google_Analytics_User_Model
import httplib2
from oauth2client.client import flow_from_clientsecrets, Credentials
import json
from datetime import datetime, timedelta 
from database import db

class Google_Analytics_API:

	def __init__(self, username):
		"""
		Creates a Google Analytics API object with a username based on stored credentials or by retrieving credentials via OAuth2 if user has not yet stored credentials or they have expired.

		args:
			username: username on the Lean Workbench sites
		"""
		# get latest credentials
		print 'username '
		print username
		self.credentials = Google_Analytics_User_Model.query.filter_by(username = username).all()
		print self.credentials
		if self.credentials:
			self.credentials = self.credentials[-1]
			expires_on = self.credentials.as_dict()['token_expiry']
			current_time = datetime.now().isoformat()
			print 'expires_on ' + str(expires_on)
			print 'current_time ' + str(current_time)
			# if valid credentials are in the database
			if expires_on > current_time:
				print 'expires on is greater than the current time'
				self.client = self.build_client(self.credentials)
			else:
				print 'crdentials expired'
				print self.credentials
				credentials_dict = self.credentials.as_dict()
				self.refresh_token(credentials_dict.get("refresh_token"), credentials_dict.get("client_id"), credentials_dict.get("client_secret"))
				self.client = self.build_client(self.credentials)
		else:
			print "no credentials"
			return None

	def refresh_token(self,refresh_token,client_id, client_secret):
		"""
		Refresh the access token if expired
		"""
		url = 'https://accounts.google.com/o/oauth2/token'
		values = {"refresh_token":refresh_token, "client_id":client_id, "client_secret":client_secret, "grant_type":"refresh_token"}
		# encode data
		print values
		data = urllib.urlencode(values)
		# post request for refresh token
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		print response
		response_json = json.loads(response.read())
		new_access_token = response_json["access_token"]
		new_expiration_date = str(datetime.now() + timedelta(1))
		self.credentials.token_expiry = new_expiration_date
		db.session.commit()

	def build_client(self, ga_user_credentials):
		print 'build client'
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
		print redirect_url	
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
		db.session.close()

	def get_user_accounts(self):
		accounts = self.client.management().accounts().list().execute()
		return accounts

	def get_profile_id(self):
		account_id = self.get_user_accounts().get('items')[-1].get('id')
		print account_id
		webproperties = self.client.management().webproperties().list(accountId=account_id).execute()
		if webproperties.get('items'):
		# Get the first Web Property ID
			firstWebpropertyId = webproperties.get('items')[0].get('id')

		# Get a list of all Profiles for the first Web Property of the first Account
		profiles = self.client.management().profiles().list(
          accountId=account_id,
          webPropertyId=firstWebpropertyId).execute()

		return profiles.get('items')[0].get('id')
