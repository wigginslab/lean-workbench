from flask.ext.restful import fields, marshal_with
import sys
import os
from user_model import User
from flask.ext.restful import Resource, reqparse
from flask import session, escape, abort, jsonify
from flask.ext.security import auth_token_required, current_user


path = os.getenv("path")
sys.path.append(path)


class User_resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
	def get(self, **kwargs):
		if not current_user.is_authenticated():
			return jsonify(message='Unauthorized', status_code=200)
		else:
			return jsonify(onboarded=current_user.onboarded)
		return {"status":200, "hypotheses":hypotheses}	
	def post(self, **kwargs):
		return Hypothesis_DAO.add_user_hypothesis(kwargs)
