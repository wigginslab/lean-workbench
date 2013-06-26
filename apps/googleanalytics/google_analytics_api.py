import httplib2

from apiclient.discovery import build

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

import sys
import json

#import the Auth Helper class
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

class Google_analytics_API:

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

		FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
  		scope='https://www.googleapis.com/auth/analytics.readonly',
  		message=MISSING_CLIENT_SECRETS_MESSAGE)

		TOKEN_FILE_NAME = 'analytics.dat'
		storage = Storage(TOKEN_FILE_NAME)
		credentials = storage.get()
		if not credentials or credentials.invalid:
			credentials = run(FLOW, storage)
		return credentials

	def initialize_service(self):
		http = httplib2.Http()

		# get stored credentials or run auth flow if none are found
		credentials = self.prepare_credentials()
		http = credentials.authorize(http)

		# construct and return the authorized Analytics Service Object
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

Google_analytics_API()
