from database import db
import datetime



class WufooSurveyModel(db.Model):
    __tablename__ = "wufoo_survey"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    name = db.Column(db.String)
    fields = db.relationship("WufooFieldModel", backref='wufoo_survey', lazy='dynamic')
    url = db.Column(db.String)
    # Lean Workbench username
    username = db.Column(db.String)
    # wufoo email
    wufoo_email = db.Column(db.String)
    handshake = db.Column(db.String)
    # responses to survey
    entries = db.relationship('WufooEntryModel', backref='wufoo_survey', lazy='dynamic')
    textareas = db.relationship('WufooTextareaSentiment', backref='wufoo_survey', lazy='dynamic')

    def __init__(self, name=None, url=None, username=None, wufoo_email=None, handshake=None):
        self.created = datetime.datetime.now()
        self.name = name 
        self.url = url
        self.username = username
        self.wufoo_email = wufoo_email
        self.handshake = handshake
    def as_dict(self):

        return {
            'id': self.id,
            'name': self.name,
            'fields': [x.as_dict() for x in self.fields.all()],
            'url': self.url,
            'username': self.username,
            'entries': [x.as_dict() for x in self.entries.all()]
        }

class WufooTextareaSentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('wufoo_survey.id'))
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    score = db.Column(db.Float(15), default=0.0)
    sentiment_type = db.Column(db.String)
    text = db.Column(db.Text)

    def __init__(self,score,sentiment_type, text):
        self.score = score
        self.sentiment_type = sentiment_type
        self.text = text

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
    values = db.relationship("WufooValueModel", backref="wufoo_field", lazy="dynamic")
    entries =  db.relationship("WufooEntryModel", backref="wufoo_field", lazy="dynamic")
    subfields = db.relationship("WufooSubfieldModel", backref="wufoo_field", lazy='dynamic')

    def __init__(self, survey_id=None, value=None, label=None, field_type=None, field_id=None, title=None):
        self.survey_id = survey_id
        self.value = value
        self.label = label
        self.field_type = field_type
        self.field_id = field_id
        self.title= title

    def as_dict(self):
        return {
            'field_id': self.field_id,
            'title': self.title,
            'field_type': self.field_type,
            'values': [x.as_dict() for x in self.values],
            'subfields': [x.as_dict() for x in self.subfields]
        }

class WufooSubfieldModel(db.Model):
    __tablename__ = "wufoo_subfield"
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.String)
    label = db.Column(db.String)
    field_field_id = db.Column(db.Integer, db.ForeignKey('wufoo_field.id'))
    values = db.relationship("WufooValueModel", backref="wufoo_subfield", lazy="dynamic")

    def as_dict(self):
        return {
                "field_id":self.field_id,
                "label": self.label,
                "values": [x.as_dict() for x in self.values]
                }
class WufooEntryModel(db.Model):
    """
    A user's survey response
    """
    __tablename__ = "wufoo_entry"
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.String)
    survey_id = db.Column(db.ForeignKey('wufoo_survey.id'))
    values = db.relationship("WufooValueModel", backref="survey", lazy="dynamic")
    field_id = db.Column(db.ForeignKey('wufoo_field.id'))

    def as_dict(self):
        return {
            'values':[value.as_dict() for value in self.values]
                }
class WufooValueModel(db.Model):
    """
    Values to an entry
    """
    __tablename__ = "wufoo_value"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    entry_id = db.Column(db.Integer, db.ForeignKey('wufoo_entry.id'))
    wufoo_field_id = db.Column(db.Integer, db.ForeignKey('wufoo_field.id'))
    wufoo_subfield_id = db.Column(db.Integer, db.ForeignKey('wufoo_subfield.id'))

    def __init__(self,value):
        self.value = value

    def __repr__(self):
        return self.value

    def as_dict(self):
        return {
                "value":self.value
                }
