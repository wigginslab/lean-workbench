import httplib2

from apiclient.discovery import build
from flask import session, Flask, redirect
from oauth2client.client import flow_from_clientsecrets
from storage import Storage
from oauth2client.tools import run
#from models.google_analytics_model import Google_Analytics_Model
import sys
import json
#from app import db

#import the Auth Helper class
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')
app.debug = True


class Google_analytics_oauth:

	def __init__(self):
		"""
		Initialize the service object
		"""
		self.prepare_credentials()
		self.service = self.initialize_service()
		profile_id = self.get_a_profile()
		print profile_id
		print self.get_results(profile_id)
		
	def prepare_credentials(self):
		
		CLIENT_SECRETS = 'client_secrets.json'
		MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

		flow= flow_from_clientsecrets(CLIENT_SECRETS,
  		scope='https://www.googleapis.com/auth/analytics.readonly',
  		message=MISSING_CLIENT_SECRETS_MESSAGE)

		#TOKEN_FILE_NAME = 'analytics.dat'
		#storage = Storage()
		#credentials = storage.get()
		#if not credentials or credentials.invalid:
		
		
		#credentials = run(FLOW, storage)
		oauth_callback = "/connect/google-analytics/callback" 
		flow.redirect_uri = oauth_callback
		authorize_url = flow.step1_get_authorize_url()
		redirect("/connect/google-analytics/callback",code=302)	


	def initialize_service(self):
		http = httplib2.Http()

		# get stored credentials or run auth flow if none are found
		credentials = self.prepare_credentials()
		http = credentials.authorize(http)

		# construct and return the authorized Analytics Service Object
		print  build('analytics', 'v3', http=http)

		return build('analytics', 'v3', http=http)

	def get_a_profile(self):
		"""
		Get all of the users' google analytics profiles
		"""
		accounts = self.service.management().accounts().list().execute()
		accountId = accounts['items'][4]['id']

		webproperties = self.service.management().webproperties().list(accountId=accountId).execute()
		print 'webproperties'
		print webproperties
		print webproperties.keys()
		if 'items' in webproperties.keys():
			#get the first web property
			firstWebpropertyId = webproperties['items'][0]['id']

			profiles = self.service.management().profiles().list(
					accountId=accountId,
					webPropertyId=firstWebpropertyId).execute()

			if profiles.get('items'):
				# return first profile ID
				print profiles.get('items')[0].get('id')
				return profiles.get('items')[0].get('id')

	def get_results(self, profile_id):
		"""
		"""
		print profile_id

		#return json.dumps( self.service.data().ga().get(
		#		ids="ga:" + profile_id,
		#		start_date='2013-06-03',
		#		end_date='2013-06-20',
		#		metrics='ga:visits').execute())
		return json.dumps( self.service.data().ga().get(
				ids="ga:" + profile_id,
				start_date='2013-06-03',
				end_date='2013-06-20',
				metrics='ga:percentNewVisits').execute())

Google_analytics_oauth()
