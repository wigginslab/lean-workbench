from flask.ext.restful import fields, marshal_with
import sys
import os
from hypotheses_model import HypothesisModel, db
from flask.ext.restful import Resource, reqparse
from flask import session, escape, abort, jsonify, request
from flask.ext.security import auth_token_required, current_user
from werkzeug.exceptions import Unauthorized
import json
import sys
sys.path.append('..')
from twitter.twitter_mine import *
from google_analytics.ga_mine import *

path = os.getenv("path")
sys.path.append(path)

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('title', type=str)
parser.add_argument('google_analytics', type=str)
parser.add_argument('wufoo', type=str)
parser.add_argument('event', type=str)
parser.add_argument('social', type=str)
parser.add_argument('facebook', type=str)
parser.add_argument('twitter', type=str)
parser.add_argument('end_time', type=str)
parser.add_argument('start_time', type=str)

from werkzeug.exceptions import Unauthorized


class HypothesisDAO(object):
	"""
	Hypothesis Data Access Object
	used to query the Hypothesis  models for the Resource

	args:
		username: required
	"""
	def __init__(self, username, profile_id=None):
		self.username = username
		self.profile_id = profile_id
		
	def get_user_hypotheses(self):
		hypotheses = HypothesisModel.query.filter_by(username=self.username).all()
		hypotheses_list = [hyp.serialize for hyp in hypotheses]
		return hypotheses_list

	def add_user_hypothesis(self, form_dict):
		title = form_dict.get('title')
		google_analytics = form_dict.get('google_analytics')
		wufoo = form_dict.get('wufoo')
		twitter = form_dict.get('twitter')
		facebook = form_dict.get('facebook')
		event = form_dict.get('event')
		start_date = form_dict.get('start_date')
		end_date = form_dict.get('end_date')
		endpoint = os.getenv('endpoint')
		print google_analytics
		print title
		hypothesis = HypothesisModel({"username":self.username,
				"wufoo":wufoo,
				"event":event,
				"twitter":twitter,
				"facebook":facebook,
				"creation_date":start_date,
				"end_date":end_date,
				"title":title,
				"endpoint":endpoint,
				"google_analytics":google_analytics
			}
		)
		db.session.add(hypothesis)
		db.session.commit()
		db.session.close()
		# if twitter data exists
		if twitter:
			# mine it
			pass

		if google_analytics:
			# mine it
			pass
		return jsonify(status=200)

	def get_a_hypothesis(self, **form_dict):
		hyp_id = form_dict.get('id')
		# TODO: make query better
		return HypothesisModel.query.filter_by(username=self.username).get_all()[hyp_id]

class HypothesisResource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	def get(self, **kwargs):
		if not current_user.is_authenticated():
			return jsonify(message='Unauthorized', status_code=400)
		args = parser.parse_args()
		print current_user
		username = current_user.email
		hypotheses = HypothesisDAO(username).get_user_hypotheses()	
		return jsonify(status=200, hypotheses = hypotheses,onboarded=current_user.onboarded)

	def post(self):
		username = current_user.email
		hypothesis = HypothesisDAO(username)
		print hypothesis
		print request.json
		return hypothesis.add_user_hypothesis(request.json)