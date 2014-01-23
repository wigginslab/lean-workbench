from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db
import datetime

counts = db.Table('tweet_counts',
		db.Column('date_count_id', db.Integer, db.ForeignKey('date_count.id')),
		db.Column('word_id', db.Integer, db.ForeignKey('word.id'))
)

tracked_twitter_words = db.Table('tracked_twitter_words',
	db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
	db.Column('twitter_id', db.Integer, db.ForeignKey('twitter.id'))
)

class Date_count(db.Model):

	__tablename__ = "date_count"
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.now())
	count = db.Integer()

class Word(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(140))
	counts = db.relationship('date_count', secondary =counts, backref=db.backref('words', lazy='dynamic'))

class Twitter_model(db.Model):

	__tablename__ = "twitter"
	id = db.Column(db.Integer, primary_key=True)
	oauth_token = db.Column(db.String)
	oauth_token_secret = db.Column(db.String)
	username = db.Column(db.String)
	twitter_handle = db.Column(db.String)
	words =  db.relationship('words', secondary=tracked_twitter_words,
		backref=db.backref('Twitter_model'))

	def __init__(self, cred_dict):
		self.oauth_token =  cred_dict.get('oauth_token')
		self.oauth_token_secret = cred_dict.get('oauth_token_secret')
		self.username = cred_dict.get('username')
		self.twitter_handle = cred_dict.get('twitter_handle')

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __str__(self):
		return "%s" %(self.username)
