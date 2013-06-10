from flask import Flask
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
Base = declarative_base()

# many to many associations
company_competitors_asssociation = Table('company_competitiors_assocation', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('competitors_id', Integer, ForeignKey('company.id')))

company_tags_association = Table('company_tags_association', Base.metadata,
	Column('company_id', Integer, ForeignKey('company.id')),
	Column('tag_id', Integer, ForeignKey('tag.id')))

company_employees_association =  Table('company_employees_association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('person_id', Integer, ForeignKey('person.id')))

company_investors_association = Table('company_investors_association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('person_id', Integer, ForeignKey('person.id')))

company_milestones_association =  Table('company_milestone_association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('milestone_id', Integer, ForeignKey('milestone.id')))

class Company(Base):
	__tablename__ = "company"
	id = db.Column(Integer, primary_key=True)
	investors = db.relationship("Person", secondary=company_investors_association)
	tags = db.relationship("Tag", secondary=company_tags_association)
	employees = db.relationship("Person", secondary=company_employees_association)
	number_of_employees = db.Column(Integer)
	founded_year =  db.Column(Integer(4))
	founded_month = db.Column(db.Integer)
	founded_day = db.Column(db.Integer)
	image= db.Column(db.String)
	milestones=db.relationship("Milestone", secondary=company_milestones_association)

class Person(Base):
	"""
	For investors and/or employees and/or founders
	"""
	__tablename__= "person"
	id = db.Column(Integer, primary_key=True)
	name = db.Column(db.String(80))
	crunchbase_url=db.Column(db.String(100))
	birthday= db.Column(db.String(10))
	image = db.Column(db.String)
	degree = relationship("Degree", backref="person")


class Degree(Base):
	"""
	One to Many relationship with Person
	"""
	__tablename__= "degree"
	id = db.Column(Integer, primary_key=True)
	school = Column(db.String)
	degree_type = db.Column(db.String)
	person_id=Column(Integer, ForeignKey('person.id'))

class InvestmentRound(Base):
	__tablename__ = "investmentRound"
	id = db.Column(db.Integer, primary_key=True)
	round_code = db.Column(db.String)
	funded_day = db.Column(db.String)
	funded_month = db.Column(db.String)
	funded_year = db.Column(db.String)

class Milestone(Base):
	"""
	Startup milestones
	"""
	__tablename__= "milestone"
	id = Column(Integer, primary_key=True)
	year = db.Column(db.Integer)
	month = db.Column(db.Integer)
	day = db.Column(db.Integer)
	url = db.Column(db.String)



class Tag(db.Model):
	"""
	Company semantic tags
	"""
	__tablename__ = "tag"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

class Role(Base):
	"""
	Role of a person in a company
	"""
	__tablename__ = "role"
	id = Column(db.Integer, primary_key=True)
	person_id = Column(db.Integer, ForeignKey('person'))