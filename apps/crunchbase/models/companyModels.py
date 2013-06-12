from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.sqlalchemy import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

# many to many associations

company_investors_association = db.Table('company_investor_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)

company_tags_association = db.Table('company_tags_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

company_employees_association = db.Table('company_employees_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)

company_milestones_association = db.Table('company_milestones_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('miletstone_id', db.Integer, db.ForeignKey('milestone.id'))
)

company_competitors_association = db.Table('company_competitors_association',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'))
)

investments_investor_association = db.Table('investments_investor_association',
    db.Column('investment_round_id', db.Integer, db.ForeignKey('investment_round.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'))
)

class Company(db.Model):
	__tablename__ = "company"
	id = db.Column(db.Integer, primary_key = True)
	investors = db.relationship("Person", secondary = company_investors_association)
	tags = db.relationship("Tag", secondary = company_tags_association)
	employees = db.relationship("Person", secondary=company_employees_association)
	number_of_employees = db.Column(Integer)
	founded_year =  db.Column(Integer(4))
	founded_month = db.Column(db.Integer)
	founded_day = db.Column(db.Integer)
	image= db.Column(db.String)
	milestones=db.relationship("Milestone", secondary=company_milestones_association)

class Person(db.Model):	
	"""
	For investors and/or employees and/or founders
	"""
	__tablename__= "person"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	crunchbase_url = db.Column(db.String(100))
	birthday = db.Column(db.String(10))
	image = db.Column(db.String(100))
#	degree = relationship("Degree", backref="person")

	def __init__(self,name=None, crunchbase_url=None, birthday=None, image=None):
		self.name = name
		self.crunchbase_url = crunchbase_url
		self.birthday = birthday
		self.image = image

class Tag(db.Model):
	"""
	Company semantic tags
	"""
	__tablename__ = "tag"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self, name=None):
		self.name = name

class Role(db.Model):
	"""
	Role of a person in a company
	"""
	__tablename__ = "role"
	id = Column(db.Integer, primary_key=True)
	company_name = Column(db.String(100))
	role_name = db.Column(db.String(20))

class Degree(db.Model):
	"""
	One to Many relationship with Person
	"""
	__tablename__= "degree"
	id = db.Column(Integer, primary_key	=True)
	school = Column(db.String)
	degree_type = db.Column(db.String)
	person_id= db.Column(db.Integer, ForeignKey('person.id'))

class Investment_round(db.Model):
	__tablename__ = "investment_round"
	id = db.Column(db.Integer, primary_key=True)
	round_code = db.Column(db.String)
	funded_day = db.Column(db.String)
	funded_month = db.Column(db.String)
	funded_year = db.Column(db.String)
	investors = db.relationship("Person", secondary=investments_investor_association)

class Milestone(db.Model):
	"""
	Startup milestones
	"""
	__tablename__= "milestone"
	id = db.Column(Integer, primary_key=True)
	name = db.Column(db.String)
	year = db.Column(db.Integer)
	month = db.Column(db.Integer)
	day = db.Column(db.Integer)
	url = db.Column(db.String)


