from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db
import datetime

tracked_twitter_words = db.Table('twitter_tracked_words',
	db.Column('twitter_word_id', db.Integer, db.ForeignKey('twitter_word.id')),
	db.Column('twitter_id', db.Integer, db.ForeignKey('twitter.id'))
)

class Date_count(db.Model):

	__tablename__ = "twitter_date_count"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.now())
	count = db.Column(db.Integer)
	word_id = db.Column(db.Integer, db.ForeignKey('twitter_word.id'))

	def as_dict(self):
		return {
			'id':self.id,
			'date':str(self.date),
			'count':self.count
		}

class Word(db.Model):
	__tablename__ = "twitter_word"
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(140))
	counts = db.relationship('Date_count',  backref='twitter_word', lazy='dynamic')
	


	def as_dict(self):
		return {
			'id': self.id,
			'word': self.word,
			'counts': [c.as_dict() for c in self.counts]
		}

class Twitter_model(db.Model):

	__tablename__ = "twitter"
	id = db.Column(db.Integer, primary_key=True)
	oauth_token = db.Column(db.String)
	oauth_token_secret = db.Column(db.String)
	# LWB email
	username = db.Column(db.String)
	twitter_handle = db.Column(db.String)
	words =  db.relationship('Word', secondary=tracked_twitter_words,
		backref=db.backref('Twitter_model'))

	def __init__(self, cred_dict):
		self.oauth_token =  cred_dict.get('oauth_token')
		self.oauth_token_secret = cred_dict.get('oauth_token_secret')
		self.username = cred_dict.get('username')
		self.twitter_handle = cred_dict.get('twitter_handle')
		company_name = cred_dict.get('company')
		self.words = [(Word(word=company_name))]

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __str__(self):
		return "%s" %(self.username)
