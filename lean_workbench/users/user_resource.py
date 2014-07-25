from flask.ext.restful import fields, marshal_with
import sys
import os
from user_model import User, Role
from flask.ext.restful import Resource, reqparse
from flask import jsonify, request
from flask.ext.security import auth_token_required, current_user
from mine import *
from database import db

path = os.getenv("path")
sys.path.append(path)


class User_resource(Resource):
	"""
	Handles requests and returns the resources they ask for
	"""
        
	def get(self, **kwargs):
                users = User.query.all()
                for user in users:
                        print user.as_dict()

	        if not current_user.is_authenticated():
			return jsonify(message='Unauthorized', status_code=200)

	def post(self, **kwargs):
		args = request.json
		onboarded = args.get('onboarded')
                cohort_name = args.get('cohort')
		if onboarded:
			return jsonify(status=200)
                elif cohort_name:
                    cohort_model = Role.query.filter_by(name=cohort_name).first()
                    if not cohort_model:
                        cohort_model = Role(name=cohort_name)
                    # add cohort to user
                    db.session.add(cohort_model)
                    current_user.roles.append(cohort_model)
                    db.session.add(current_user)
                    db.session.commit()
		else:
			print 'not onboarded'
			return jsonify(status=200)
