import sys
import os
from twitter_model import Twitter_model
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify
import os
from database import db
from flask.ext.security import current_user


class Twitter_DAO(object):

	def __init__(self):
		self.user_twitter = Twitter_model.query.filter_by(username=current_user.email).first()
		self.twitter_handle = self.user_twitter.twitter_handle
	def as_dict(self):
		return self.user_twitter.as_dict()

class Twitter_resource(Resource):
	def get(self, **kwargs):
		twitter = Twitter_DAO()
		if twitter.user_twitter:
			print twitter.user_twitter
			return jsonify({'twitter_handle':twitter.twitter_handle})
		else:
			return []

