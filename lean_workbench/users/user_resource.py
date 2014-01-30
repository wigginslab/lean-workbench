from flask.ext.restful import fields, marshal_with
import sys
import os
from user_model import User, db
from flask.ext.restful import Resource, reqparse
from flask import jsonify, request
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

	def post(self, **kwargs):
		args = request.json
		onboarded = args.get('onboarded')
		if onboarded:
			print 'onboarded'
			current_user.onboarded = True
			db.session.commit()
			db.session.close()
		else:
			print 'not onboarded'
