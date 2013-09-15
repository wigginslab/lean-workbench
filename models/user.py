from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys
import uuid
from flask.ext.security import UserMixin, RoleMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

apis = db.Table('apis',
		db.Column('api_id', db.Integer, db.ForeignKey('api.id')),
		db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60))
	password = db.Column(db.String())
	created = db.Column(db.DateTime())
	last_login_at = db.Column(db.DateTime())
	current_login_at = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String())
	current_login_ip = db.Column(db.String())
	login_count = db.Column(db.Integer())
	created = db.Column(db.Date())
	company = db.Column(db.String)
	apis = db.relationship('API', secondary=apis,backref=db.backref('apis', lazy='dynamic'))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Role', secondary=roles_users,
			backref=db.backref('user', lazy='dynamic'))
	"""
	def __init__(self, email, password, active, company, roles, apis=[]):
		self.email = email
		self.company = company
		self.activate = True
		self.created = datetime.utcnow()
		self.apis = apis
		self.active = active
		self.roles = roles

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)
		
	def check_username(self):
		sameUsername = User.query.filter_by(username=self.username).all()
		print 'sameUsername: '
		print sameUsername
		if sameUsername: 
			abort(401)
	"""
	"""
	def change_password(self, username, new_password):
		self.pwdhash = generate_password_hash(new_password)

	def __repr__(self):
		return '<User %s>' %self.username
	"""
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
