from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

twitter_words_association = db.Table('twitter_words_association',
    db.Column('twitter_id', db.Integer, db.ForeignKey('twitter_credentials.id')),
    db.Column('word_id', db.Integer, db.ForeignKey('word.id'))
)

class Twitter_model:
	
	__tablename__ = "twitter_credentials"

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
	words = roles = db.relationship('word', secondary=roles_users,
			backref=db.backref('twitter_credentials')