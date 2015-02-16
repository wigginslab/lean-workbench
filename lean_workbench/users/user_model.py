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
from database import db
from google_analytics.google_analytics_models import GoogleAnalyticsReturningVisitors, GoogleAnalyticsSignups

apis = db.Table('apis',
		db.Column('api_id', db.Integer, db.ForeignKey('api.id')),
		db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

returning_visitors = db.Table('user_google_analytics_returning_visitors',
	  	db.Column('user_id', db.Integer(), 
	  	db.ForeignKey('user.id')),
        db.Column('google_analytics_returning_visitors_id', 
        db.Integer(), 
        db.ForeignKey('google_analytics_returning_visitors.id')))

signups = db.Table('user_google_analytics_returning_signups',
	  	db.Column('user_id', db.Integer(), 
	  	db.ForeignKey('user.id')),
        db.Column('google_analytics_signups_id', 
        db.Integer(), 
        db.ForeignKey('google_analytics_signups.id')))

class Role(db.Model, RoleMixin):
	"""
	Cohorts
	"""
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))
	    
	def __repr__(self):
		return self.name

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
	onboarded = db.Column(db.Boolean(), default=False)
	returning_visitors = db.relationship('GoogleAnalyticsReturningVisitors', 
		secondary=returning_visitors,
		backref=db.backref('user')
	)
	signups = db.relationship('GoogleAnalyticsSignups', 
	secondary=signups,
	backref=db.backref('user')
	)
		
		
	def __repr__(self):
		return '<User %s>' %self.email

        def as_dict(self):
                return {
                        'email':self.email,
                        'roles':[str(role) for role in self.roles],
                        'onboarded': self.onboarded
                }
class API(db.Model):
	__tablename__ = "api"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	endpoint = db.Column(db.String)

	def __init__(self, name, endpoint=None):
		self.name = name
		self.endpoint = endpoint
