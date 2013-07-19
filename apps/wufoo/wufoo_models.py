from datetime import datetime
from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)


class Wufoo_Survey_Model(db.Model):
	__tablename__ = "wufoo_survey"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	fields = db.relationship("Wufoo_Field_Model", backref='wufoo_survey', lazy='dynamic')
	url = db.Column(db.String)

class Wufoo_Field_Model(db.Model):
	__tablename__ = "wufoo_field"

	id = db.Column(db.Integer, primary_key=True)
	survey_id = db.Column(db.Integer, db.ForeignKey('wufoo_survey.id'))
#	choices = db.relationship('Wufoo_Choice_model', backref='wufoo_field',lazy='dynamic')
	# if text response and not choice
	value = db.Column(db.String, primary_key=True)
"""
class Wufoo_Choice_Model(db.Model):
	__tablename__ = "wufoo_choice"

	id = db.Column(db.Integer, primary_key=True)
	# name of choice
	label = db.Column(db.String)
	field_id = db.Column(db.Integer, db.ForeignKey('wufoo_field.id'))

class Wufoo_IP_Model(db.Model):
	__tablename__ = "wufoo_ip"

	id = db.Column(db.Integer, primary_key=True)
	ip = db.Column(db.String)
"""
