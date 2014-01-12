import sys
import os
from twitter_model import Twitter_model
from flask.ext.restful import Resource, reqparse
from flask import Flask
import os
from database import db

class Twitter_DAO(object):

	def __init__():
		self.user_twitter = Twitter_model(username=current_user).first()

class Twitter_resource(Resource):
	def get(self, **kwargs):
		twitter = Twitter_DAO()
		if twitter.user_twitter:
			print self.user_twitter
			return self.user_twitter
		else:
			return []

