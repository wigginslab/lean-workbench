import sys
import os
from facebook_model import Facebook_model
from database import db
from flask.ext.restful import Resource, reqparse, fields, marshal_with, abort
from flask.ext.security import current_user

class Facebook_DAO(object):

	def __init__(self):
		self.user_facebook = Facebook_model.query.filter_by(username=current_user.email).first()

class Facebook_resource(Resource):
	def get(self, **kwargs):
		fb = Facebook_DAO()
		if fb.user_facebook:
			return [fb.user_facebook]
		else:
			return []


	