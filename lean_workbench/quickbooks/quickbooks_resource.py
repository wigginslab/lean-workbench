import sys
import os
from quickbooks_model import Quickbooks_model
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request
import os
from database import db
from flask.ext.security import current_user


class Quickbooks_DAO(object):

	def __init__(self):
		self.user_qb = Quickbooks_model.query.filter_by(username=current_user.email).first()


	def as_dict(self):
		return self.user_qb.as_dict()

class Quickbooks_resource(Resource):
	def get(self, **kwargs):
		#return jsonify(twitter_authed=True)
		qb = Quickbooks_DAO()
		if qb.user_qb:
			print qb.user_qb
		
			return jsonify(qb_authed=True)
		else:
			return jsonify(qb_authed=False)

	def post(self):
		
		return jsonify(qb_authed=True)
