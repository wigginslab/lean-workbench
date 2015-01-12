import urllib
import urllib2
import os
from apiclient.discovery import build
from google_analytics_models import GoogleAnalyticsUserModel
import httplib2
from oauth2client.client import flow_from_clientsecrets, Credentials
import json
from datetime import datetime, timedelta 
from database import db
from flask import current_app
import sys

class GoogleAnalyticsAPI:

	def __init__(self, username):
		"""
		Creates a Google Analytics API object with a username based on stored credentials or by retrieving credentials via OAuth2 if user has not yet stored credentials or they have expired.

		args:
			username: username on the Lean Workbench sites
		"""
                self.client = None
		# get latest credentials
		self.credentials = GoogleAnalyticsUserModel.query.filter_by(username = username).first()
                print self.credentials
		if self.credentials:
                        print 'there  are ga  credentials'
                        
		        expires_on = self.credentials.token_expiry
                        print 'expires on' + str(expires_on)
			current_time = datetime.now()
                        print 'current_time '+str(current_time)
                        credentials_dict = self.credentials.as_dict()
                        self.credentials_dict = credentials_dict
                        print 'about to compare times'
                        if current_time > expires_on:
                            print 'credentials dict:'
                            print self.credentials_dict
                            print 'about to refresh token'
                            self.refresh_token(credentials_dict.get("refresh_token"), credentials_dict.get("client_id"), credentials_dict.get("client_secret"))
                            print 'GA credentials: ' + str(self.credentials_dict)
                        else: 
                            self.refresh_token(credentials_dict.get("refresh_token"), credentials_dict.get("client_id"), credentials_dict.get("client_secret"))

                        self.client = self.build_client()
		else:
			print "no GA  credentials"
			return None

	def refresh_token(self,refresh_token=None,client_id=None, client_secret=None):
		"""
		Refresh the access token if expired
		"""
                if not refresh_token and not client_id:
                    refresh_token = self.credentials.refresh_token
                    client_id = self.credentials.client_id
                    client_secret = self.credentials.client_secret

		url = 'https://accounts.google.com/o/oauth2/token'
                values = {"refresh_token":refresh_token, "client_id":client_id, "client_secret":client_secret, "grant_type":"refresh_token"}
                print 'refresh_token POST values: ' + str(values)
	        # encode data
		data = urllib.urlencode(values)
                print 'changed'
                print 'data:' + str(data)
		# post request for refresh token
		req = urllib2.Request(url, data)
                print  req.get_full_url()
                response = urllib2.urlopen(req)
                print 'response: ' + str(response)
                response_json = json.loads(response.read())
                print 'google refresh token response json: ' + str(response_json)
                new_access_token = response_json["access_token"]
                self.credentials.access_token = new_access_token
                new_expiration_date = datetime.now() + timedelta(hours=1)
                self.credentials.token_expiry = new_expiration_date
                db.session.add(self.credentials)
                db.session.commit()
                print 'done getting values from fresh_token'

	def build_client(self):
		print 'build client'
		credential_dict = self.credentials.as_dict()
                print 'credentials: '
                print credential_dict
		credential_dict['_module'] = "oauth2client.client"
		credential_dict['_class'] = "OAuth2Credentials"
		credential_dict['token_uri'] = "https://accounts.google.com/o/oauth2/auth?approval_prompt=force"
		credential_dict['user_agent'] = "null"
                credential_dict['access_type'] = "offline"
		credential_dict['invalid'] = "false"
                credential_dict['token_expiry'] = "T".join(str(credential_dict['token_expiry']).split(" ")).split(".")[0]
                print credential_dict['token_expiry']
		credentials = Credentials.new_from_json(json.dumps(credential_dict))
		http = httplib2.Http()
                print 'credentials built'
		http = credentials.authorize(http)  
		#  Build the Analytics Service Object with the authorized http object
		client = build('analytics', 'v3', http=http)
                print 'client built'
		return client

	def step_one(self, google_analytics_callback_url, google_analytics_client_id):
		"""
		Construct URL for user to login to Google through. 

		Returns:
			redirect url
		"""
		redirect_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/analytics.readonly&access_type=offline&redirect_uri="+google_analytics_callback_url+"&client_id="+google_analytics_client_id+"&hl=en&from_login=1&as=819ec18979456db&pli=1&authuser=0"
		print redirect_url	
		return redirect_url

	def step_two(self,username, ga_api_code, google_analytics_callback_url):
		"""
		Handle callback information
		"""
                print 'redirect_uri %s' %(google_analytics_callback_url)
		client_secrets = "/var/www/lean-workbench/lean_workbench/google_analytics/ga_client_secrets.json"
		flow = flow_from_clientsecrets(client_secrets,
						scope='https://www.googleapis.com/auth/analytics.readonly',
								message='%s is missing' % client_secrets, redirect_uri=google_analytics_callback_url)
		credentials = flow.step2_exchange(code=str(ga_api_code))
		credentials_json = json.loads(credentials.to_json())
		credentials_json['username'] = username
		print credentials_json
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
                credentials_dict['token_expiry'] = datetime.now() + timedelta(hours=1)
		GAUM = GoogleAnalyticsUserModel(credentials_dict)
		db.session.add(GAUM)
		db.session.commit()
		db.session.close()

	def get_user_accounts(self):
            print 'inside get_user_accounts'
            print self.client
            accounts = self.client.management().accounts().list().execute()
            print 'user accounts: '
            print accounts
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
