from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db


class Word(db.Model):
	__tablename__ = "Words"

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(140))

class Twitter_model(db.Model):
	__tablename__ = "Twitter"

	id = db.Column(db.Integer, primary_key=True)
	oauth_token = db.Column(db.String)
	oauth_token_secret = db.Column(db.String)
	username = db.Column(db.String)
	twitter_handle = db.Column(db.String)
	#words =  db.relationship('word', secondary=twitter_keywords,
	#		backref=db.backref('twitter_credentials'))

	def __init__(self, cred_dict):
		self.oauth_token =  cred_dict.get('oauth_token')
		self.oauth_token_secret = cred_dict.get('oauth_token_secret')
		self.username = cred_dict.get('username')
		self.twitter_handle = cred_dict.get('twitter_handle')

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __str__(self):
		return "%s" %(self.username)