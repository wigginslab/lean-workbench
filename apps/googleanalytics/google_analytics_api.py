import httplib2

from apiclient.discovery import build

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

import sys

#import the Auth Helper class
import analytics_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

class Google_Analytics_API:

	def __init__(self):
		"""
		Initialize the service object
		"""
		self.prepare_credentials()
		self.service = self.initialize_service()
		self.get_all_profiles()

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


	def get_all_profiles(self):
		"""
		Get all of the users' google analytics profiles
		"""
		accounts = self.service.management().accounts().list().execute()
		print accounts
		print '\n'
		accountId = accounts['items'][0]['id']
		webproperties = self.service.management().webproperties().list(accountId=accountId).execute()
		print webproperties	
Google_Analytics_API()

