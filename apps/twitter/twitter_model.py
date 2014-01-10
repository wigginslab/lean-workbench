from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

# words to watch out for
twitter_keywords = db.Table('twitter_words',
		db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
		db.Column('twitter_user_id', db.Integer, db.ForeignKey('Twitter_model.id'))
)

class Twitter_model:
	id = db.Column(db.Integer, primary_key=True)
	token_expiry = db.Column(db.String)
	access_token = db.Column(db.String)
	client_id = db.Column(db.String)
	client_secret = db.Column(db.String)
	profile_id = db.Column(db.String)
	refresh_token = db.Column(db.String)
	revoke_uri = db.Column(db.String)
	id_token = db.Column(db.String)
	token_response = db.Column(db.String)
	username = db.Column(db.String)
	words =  db.relationship('word', secondary=twitter_keywords,
			backref=db.backref('twitter_credentials')

class Word:
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(140))