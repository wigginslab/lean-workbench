# Many-to-Many association tables

company_competitors_table = Table('association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('competitors_id', Integer, ForeignKey('company.id'))

company_tags_table = Table('association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('tag_id', Integer, ForeignKey('tag.id'))

company_employees_table =  Table('association', Base.metadata,
	db.Column('company_id', Integer, ForeignKey('company.id')),
	db.Column('person_id', Integer, ForeignKey('person.id'))

class Company(Base):
	__tablename__ = "company"
	id = db.Column(Integer, primary_key=True)
	investors = db.relationship("Person", secondary=company_investor_table)
	tags = db.relationship("tag", secondary=company_tag_table)
	employees = 
	number_of_employees = db.Column(Integer)
	founded_year =  db.Column(Integer(4))
	founded_month = db.Column(db.Integer)
	founded_day = db.Column(db.Integer)
	image= db.column(db.String)

class Person(Base):
	"""
	For investors and/or employees and/or founders
	"""
	__tablename__= "person"
	id = db.Column(Integer, primary_key=True)
	name = db.Column(db.String(80))
	crunchbase_url=db.Column(db.String(100))
	birthday= db.Column(db.String(10))
	image = db.Column(db.String))
	degree_id = Column(Integer, ForeignKey("degree_id"))
	degree = relationship("Degree")


class Degree(Base):
	"""
	One to Many relationship with Person
	"""
	__tablename__= "degree"
	id = db.Column(Integer, primary_key=True)
	school = Column(db.String)
	type = db.Column(db.String)

class Milestone(Base):
	"""
	Startup milestones
	"""
	__tablename__= "milestone"
	year = db.Column(db.Integer)
	month = db.Column(db.Integer)
	day = db.Column(db.Integer)
	url = db.Column(db.String)


class Tag(Base):
	"""
	Company semantic tags
	"""
	__tablename__ = "tag"
	id = db.Column(Integer, primary_key=True)
	name = db.Column(db.String(80))

class Role(Base):
	"""
	Role of a person in a company
	"""
	__tablename__ = "role"
	id = Column(Integer primary_key=True)
	person_id = Column(Integer, ForeignKey('person'))