from flask.ext.restful import fields, marshal_with
import sys
import os
from apps.googleanalytics.models.google_analytics_models import *
from google_analytics_client import Google_Analytics_API

path = os.getenv("path")
sys.path.append(path)
print path

class Google_Analytics_DAO(object):
	"""
	Google Analytics Data Access Object
	used to query the GA models for the Resource

	args:
		username: required
		profile_id: id of specific GA profile to query
	"""
	def __init__(self, username, profile_id=None):
		not profile_id:
			return get_user_profiles(username)
	
	def get_user_profiles(username):
		"""
		Retrieve all userprofiles of a user
		"""
		g = Google_Analytics_API(username)
		user_accounts = g.get_user_accounts()
		return user_accounts.get('items')


class Google_Analytics_Resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	#@marshal_with(resource_fields)
	def get(self, **kwargs):
		username = kwargs.get('username')
		profile_id = kwargs.get('profile_id')
		return Google_Analytics_Dao(username = username, profile_id = profile_id)
