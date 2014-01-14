from database import db

class Wufoo_Survey_Model(db.Model):
	__tablename__ = "wufoo_survey"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	fields = db.relationship("Wufoo_Field_Model", backref='wufoo_survey', lazy='dynamic')
	url = db.Column(db.String)

	def __init__(self, name=None, fields=None, url=None):
		self.name = name
		self.fields = fields
		self.url = none

class Wufoo_Field_Model(db.Model):
	__tablename__ = "wufoo_field"

	id = db.Column(db.Integer, primary_key=True)
	survey_id = db.Column(db.Integer, db.ForeignKey('wufoo_survey.id'))
	value = db.Column(db.String)
	label = db.Column(db.String)

	def __init__(self, survey_id=None, value=None, label=None):
		self.survey_id = survey_id
		self.value = value
		self.label = label
