from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

apis = db.Table('apis',
		db.Column('api_id', db.Integer, db.ForeignKey('api.id')),
		db.Column('user_id', db.Integer, db.ForeignKey('users.uid'))
)

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60))
	pwdhash = db.Column(db.String())
	activate = db.Column(db.Boolean)
	created = db.Column(db.DateTime)
	company = db.Column(db.String)
	apis = db.relationship('API', secondary=apis,backref=db.backref('apis', lazy='dynamic'))

	def __init__(self, username, password, company, apis=[]):
		self.username = username
		error = self.check_username()
		self.pwdhash = generate_password_hash(password)
		self.company = company
		self.activate = True
		self.created = datetime.utcnow()
		self.apis = apis

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)
		
	def check_username(self):
		sameUsername = User.query.filter_by(username=self.username).all()
		print 'sameUsername: '
		print sameUsername
		if sameUsername: 
			abort(401)

	def change_password(self, username, new_password):
		"""
		Reset password to new password given by user
		"""
		self.pwdhash = generate_password_hash(new_password)

	def __repr__(self):
		"""
		Representation of the user object
		"""
		return '<User %s>' %self.username

class Password_Reset(db.Model):
	__tablename__ = 'password_reset'
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60))
	reset_code = db.Column(db.String())

	def __init__(self, username=None):
		self.username = username
		self.reset_code = str(uuid.uuid4())

class API(db.Model):
	__tablename__ = "api"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	endpoint = db.Column(db.String)

	def __init__(self, name, endpoint=None):
		self.name = name
		self.endpoint = endpoint
