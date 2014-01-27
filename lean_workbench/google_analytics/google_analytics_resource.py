from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from google_analytics_models import *
from google_analytics_client import Google_Analytics_API
from flask.ext.restful import Resource, reqparse
from flask.ext.security import current_user
from flask import session, escape
from database import db

path = os.getenv("path")
sys.path.append(path)

parser = reqparse.RequestParser()
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('dimension', type=str)
parser.add_argument('metric', type=str)

class Google_Analytics_DAO(object):
	"""
	Google Analytics Data Access Object
	used to query the GA models for the Resource

	args:
		username: required
		profile_id: id of specific GA profile to query
	"""
	def __init__(self, username, profile_id=None, metric=None, dimension=None):
		self.username = username
		self.profile_id = profile_id
		self.metric = metric
		self.dimension = dimension

	def get_user_profiles(self):
		"""
		Retrieve all userprofiles of a user
		"""
		g = Google_Analytics_API(self.username)
		user_accounts = g.get_user_accounts()
		return user_accounts.get('items')

	def get_user_profile_visits(self, start_date, profile_id):
		"""
		Go as far back as you can go, then check daily
		"""
		g = Google_Analytics_API(username=self.username)
		user_profiles = g.get_user_accounts().get('items')
		profile = user_profiles[-1]
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
		print 'ga get'
		profile = Google_Analytics_User_Model.query.filter_by(username=current_user.email)
		if profile:
			GA = Google_Analytics_DAO(username = current_user.email)
			return GA.get_user_profiles()
		else:
			return jsonify(status=333)
		#	GA = Google_Analytics_DAO(username = current_user.email, profile=profile.profile_id)

			
	def post(self, **kwargs):
		"""
		Get profile-id
		"""
		print 'GA post'
		args = parser.parse_args()
		username = current_user.email
		profile_id = args.get('profile-id')
		metric = args.get('metric')
		profile_id = kwargs.get('profile-id')
		dimension = kwargs.get('dimension')

		# if just posting profile id
		if profile_id and not metric:
			ga_cred = Google_Analytics_User_Model.query.filter_by(username=current_user.username).profile_id
			ga_cred.profile_id = profile_id
			db.session.add(ga_cred)
			db.session.commit()
			db.session.close()

		if metric == "visits":
			return GA.get_user_profile_visits()


