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
		if not profile_id:
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
	method_decorators = [authenticate_api]
	#@marshal_with(resource_fields)
	def get(self, **kwargs):
		username = kwargs.get('username')
		profile_id = kwargs.get('profile_id')
		return Google_Analytics_Dao(username = username, profile_id = profile_id)
