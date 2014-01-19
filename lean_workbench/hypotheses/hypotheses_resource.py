from flask.ext.restful import fields, marshal_with
import sys
import os
from hypotheses_model import Hypothesis_model, db
from flask.ext.restful import Resource, reqparse
from flask import session, escape, abort, jsonify
from flask.ext.security import auth_token_required, current_user
from werkzeug.exceptions import Unauthorized


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


from werkzeug.exceptions import Unauthorized


class Hypothesis_DAO(object):
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
		hypotheses = Hypothesis_model.query.filter_by(username=self.username).all()
		return hypotheses

	def add_user_hypothesis(self, **kwargs):
		goal = kwargs.get('goal')
		google_analytics = kwargs.get('google_analytics')
		wufoo = kwargs.get('wufoo')
		event = kwargs.get('event')
		hypothesis = Hypothesis_Model(username=self.username,
				goal=goal,
				wufoo=wufoo,
				event=event,
				twitter=twitter,
				facebook=facebook
		)
		db.session.add(hypothesis)
		db.session.commit()
		db.session.close()
		return {"status":200}

	def get_a_hypothesis(self, **kwargs):
		hyp_id = kwargs.get('id')
		# TODO: make query better
		return Hypothesis_Model.query.filter_by(username=self.username).get_all()[hyp_id]

class Hypothesis_resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	def get(self, **kwargs):
		if not current_user.is_authenticated():
			return jsonify(message='Unauthorized', status_code=200)

		print kwargs
		args = parser.parse_args()
		print current_user
		username = current_user.email
		print username
		hypotheses = Hypothesis_DAO(username).get_user_hypotheses()	
		return {"status":200, "hypotheses":hypotheses}	
	def post(self, **kwargs):
		return Hypothesis_DAO.add_user_hypothesis(kwargs)
