from database import db

class Wufoo_Survey_Model(db.Model):
    __tablename__ = "wufoo_survey"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fields = db.relationship("Wufoo_Field_Model", backref='wufoo_survey', lazy='dynamic')
    url = db.Column(db.String)
    # Lean Workbench username
    username = db.Column(db.String)
    # responses to survey
    entries = db.relationship('Wufoo_Entry_Model', backref='wufoo_survey', lazy='dynamic')

    def __init__(self, name=None, fields=None, url=None, username=None):
        self.name = name
        self.fields = fields
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

class Wufoo_Field_Model(db.Model):
    __tablename__ = "wufoo_field"
    id = db.Column(db.Integer, primary_key=True)
    # survey id
    survey_id = db.Column(db.Integer, db.ForeignKey('wufoo_survey.id'))
    # survey question id
    field_id = db.Column(db.String)
    # survey question text
    title  = db.Column(db.String)
    field_type = db.Column(db.String)
    values = db.relationship("Wufoo_Values", backref="field", lazy="dynamic")
    entries =  db.relationship("Wufoo_Entry_Model", backref="subfields", lazy="dynamic")

    def __init__(self, survey_id=None, value=None, label=None):
        self.survey_id = survey_id
        self.value = value
        self.label = label

    def as_dict(self):
        return {
            
        }

class Wufoo_Subfield_Model(db.Model):
    __tablename__ = "wufoo_subfield"
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.String)
    label = db.Column(db.String)

class Wufoo_Entry_Model(db.Model):
    """
    A user's survey response
    """
    __tablename__ = "wufoo_entry"
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.String)
    survey_id = db.Column(db.ForeignKey('wufoo_survey.id'))
    values = db.relationship("Wufoo_Value", backref="values", lazy="dynamic")

class Wufoo_Value(db.Model):
    """
    Values to an entry
    """
    __tablename__ = "wufoo_value"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    entry_id = db.Column(db.Integer, db.ForeignKey('wufoo_entry.id'))
