from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)


company_tags_association = db.Table('company_tags_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Crunchbase_Company(db.Model):
	__tablename__ = "crunchbase_company"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	tags = db.relationship("Tag", secondary = company_tags_association)
	number_of_employees = db.Column(Integer)
	founded_year =  db.Column(Integer(4))
	founded_month = db.Column(db.Integer)
	founded_day = db.Column(db.Integer)
	image= db.Column(db.String)
	milestones=db.relationship("Tags", secondary=company_tags_association)
	crunchbase_url = db.Column(db.String)
	homepage_url = db.Column(db.String)
	# startup or finanical organization
	company_type = db.Column(db.String)
	# associated user
	username = db.Column(db.String)
	state_code = db.Column(db.String)


class Tag(db.Model):
	"""
	Company semantic tags
	"""
	__tablename__ = "tag"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self, name=None):
		self.name = names