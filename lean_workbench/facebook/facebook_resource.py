import sys
import os
from flask import jsonify
from facebook_model import Facebook_model,Facebook_page_data
from database import db
from flask.ext.restful import Resource, reqparse, fields, marshal_with, abort
from flask.ext.security import current_user

class Facebook_DAO(object):

	def __init__(self):
		self.user_facebook = Facebook_model.query.filter_by(username=current_user.email).first()

class Facebook_resource(Resource):
	def get(self, **kwargs):
		#fb = Facebook_DAO()
		# get Facebook
		facebook_user = Facebook_model.query.filter_by(username=current_user.email).first()
		
		if not facebook_user:
			return jsonify(fb_authed=False)
		else:
			facebook_page = Facebook_page_data.query.filter_by(username=current_user.email).all()
			print facebook_page
			if hasattr(facebook_page, "__iter__"):
				return jsonify(facebook_page=[x.as_dict() for x in facebook_page])
			else:
				return jsonify(facebook_page=facebook_page.as_dict)