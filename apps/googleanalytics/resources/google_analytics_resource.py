from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from apps.googleanalytics.models.google_analytics_models import *
from apps.googleanalytics.google_analytics_client import Google_Analytics_API
from flask.ext.restful import Resource
from flask import session, escape

path = os.getenv("path")
sys.path.append(path)

def check_authentication(username):
	logged_in_user = escape(session.get('username'))
	if username == logged_in_user:
		return True
	else:
		return False


def authenticate_api(func):
	def wrapper(*args, **kwargs):
		print 'in wrapper'
		logged_in_user = escape(session['username'])
		print kwargs.get('username')
		if kwargs.get('username') == logged_in_user:
			print 'true'
			return func(*args, **kwargs)
		abort(401)
	return wrapper

class Google_Analytics_DAO(object):
	"""
	Google Analytics Data Access Object
	used to query the GA models for the Resource

	args:
		username: required
		profile_id: id of specific GA profile to query
	"""
	def __init__(self, username, profile_id=None):
		self.username = username
		self.profile_id = profile_id
	
	def get_user_profiles(self):
		"""
		Retrieve all userprofiles of a user
		"""
		g = Google_Analytics_API(self.username)
		print g.credentials
		user_accounts = g.get_user_accounts()
		return user_accounts.get('items')

class Google_Analytics_Resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	#method_decorators = [authenticate_api]
	#@marshal_with(resource_fields)
	def get(self, **kwargs):
		print kwargs
		username = kwargs.get('username')
		print username
		profile_id = kwargs.get('profile_id')
		GA = Google_Analytics_DAO(username = username, profile_id = profile_id)
		return GA.get_user_profiles()