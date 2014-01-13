from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from google_analytics_models import *
from google_analytics_client import Google_Analytics_API
from flask.ext.restful import Resource, reqparse
from flask.ext.security import current_user
from flask import session, escape

path = os.getenv("path")
sys.path.append(path)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)

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
		print check_authentication(username)

	def get_user_profiles(self):
		"""
		Retrieve all userprofiles of a user
		"""
		g = Google_Analytics_API(self.username)
		print g.credentials
		user_accounts = g.get_user_accounts()
		return user_accounts.get('items')

	def get_user_profile_visits(self, start_date, profile_id):
		"""
		Go as far back as you can go, then check daily
		"""
		g = Google_Analytics_API("jen")
		user_profiles = g.get_user_accounts().get('items')
		profile = user_profiles[-1]
		profile_id = profile.get('id')
		# convert date from isoformat to GA query format
		date_created = profile.get('created').split('T')[0]
		current_date = datetime.now().timetuple()
		print current_date
		current_year = str(current_date[0])
		current_month = str(current_date[1])
		if len(current_month) < 2: current_month = '0'+current_month
		current_day = str(current_date[2])
		if len(current_day) < 2: current_day = '0'+current_day
		current_date_string = current_year + '-' +  current_month + '-' + current_day
		g.client.data().ga().get(
					  ids='ga:' + profile_id,
							start_date=start_date,
								  end_date=end_date,
										metrics='ga:visits').execute()


class Google_analytics_resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	def get(self, **kwargs):
		args = parser.parse_args()
		username = current_user.email
		print 'google analytics username: %s' %(username)
		profile_id = kwargs.get('profile_id')
		GA = Google_Analytics_DAO(username = username, profile_id = profile_id)
		return GA.get_user_profiles()