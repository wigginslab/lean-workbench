from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys
import uuid
from flask.ext.security import UserMixin, RoleMixin
from itsdangerous import URLSafeTimedSerializer
import md5

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
	"""
	User model building off of flask-registration
	"""
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60))
	password = db.Column(db.String())
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
			backref=db.backref('user'))


	def __repr__(self):
		return '<User %s>' %self.email
class API(db.Model):
	__tablename__ = "api"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	endpoint = db.Column(db.String)

	def __init__(self, name, endpoint=None):
		self.name = name
		self.endpoint = endpoint