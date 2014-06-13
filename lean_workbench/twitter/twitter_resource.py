import sys
import os
from twitter_model import Twitter_model
from flask.ext.restful import Resource, reqparse
from flask import Flask, jsonify, request
import os
from database import db
from flask.ext.security import current_user


class Twitter_DAO(object):

	def __init__(self):
		self.user_twitter = Twitter_model.query.filter_by(username=current_user.email).first()
		print self.user_twitter
		try:
			self.twitter_handle = self.user_twitter.twitter_handle
		except:
			self.twitter_handle = None

	def as_dict(self):
		return self.user_twitter.as_dict()

class Twitter_resource(Resource):
	def get(self, **kwargs):
		if current_user.is_anonymous():
			return jsonify(status=400)
		#return jsonify(twitter_authed=True)
		twitter = Twitter_DAO()
		if twitter.user_twitter:
			print twitter.user_twitter
			#return jsonify(twitter_authed=True)
			tracked_words = twitter.user_twitter.words
			return jsonify(words=[x.as_dict() for x in tracked_words])
		else:
			return jsonify(twitter_authed=False)

	def post(self):
		args = request.args()
		return jsonify(twitter_authed=True)
