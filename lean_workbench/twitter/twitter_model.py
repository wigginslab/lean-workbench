from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db

# words to watch out for
twitter_keywords = db.Table('twitter_words',
		db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
		db.Column('twitter_user_id', db.Integer, db.ForeignKey('Twitter_model.id'))
)

class Twitter_model:
	id = db.Column(db.Integer, primary_key=True)
	oauth_token = db.Column(db.String)
	oauth_secret = db.Column(db.String)
	username = db.Column(db.String)
	twitter_handle = db.Column(db.String)
	words =  db.relationship('word', secondary=twitter_keywords,
			backref=db.backref('twitter_credentials'))

class Word:
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(140))