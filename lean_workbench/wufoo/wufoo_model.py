from database import db

class WufooSurveyModel(db.Model):
    __tablename__ = "wufoo_survey"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fields = db.relationship("WufooFieldModel", backref='wufoo_survey', lazy='dynamic')
    url = db.Column(db.String)
    # Lean Workbench username
    username = db.Column(db.String)
    # responses to survey
    entries = db.relationship('WufooEntryModel', backref='wufoo_survey', lazy='dynamic')

    def __init__(self, name=None, url=None, username=None):
        self.name = name 
        self.url = url
        self.username = username
    
    def as_dict(self):

        return {
            'id': self.id,
            'name': self.name,
            'fields': self.fields,
            'url': self.url,
            'username': self.username,
            'entries': self.entries
        }

class WufooFieldModel(db.Model):
    __tablename__ = "wufoo_field"
    id = db.Column(db.Integer, primary_key=True)
    # survey id
    survey_id = db.Column(db.Integer, db.ForeignKey('wufoo_survey.id'))
    # survey question id
    field_id = db.Column(db.String)
    # survey question text
    title  = db.Column(db.String)
    field_type = db.Column(db.String)
    values = db.relationship("WufooValue", backref="wufoo_field", lazy="dynamic")
    entries =  db.relationship("WufooEntryModel", backref="wufoo_field", lazy="dynamic")

    def __init__(self, survey_id=None, value=None, label=None):
        self.survey_id = survey_id
        self.value = value
        self.label = label

    def as_dict(self):
        return {
            
        }

class WufooSubfieldModel(db.Model):
    __tablename__ = "wufoo_subfield"
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.String)
    label = db.Column(db.String)

class WufooEntryModel(db.Model):
    """
    A user's survey response
    """
    __tablename__ = "wufoo_entry"
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.String)
    survey_id = db.Column(db.ForeignKey('wufoo_survey.id'))
    values = db.relationship("WufooValue", backref="values", lazy="dynamic")
    field_id = db.Column(db.ForeignKey('wufoo_field.id'))

class WufooValue(db.Model):
    """
    Values to an entry
    """
    __tablename__ = "WufooValue"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    entry_id = db.Column(db.Integer, db.ForeignKey('wufoo_entry.id'))
    wufoo_field_id = db.Column(db.Integer, db.ForeignKey('wufoo_field.id'))
