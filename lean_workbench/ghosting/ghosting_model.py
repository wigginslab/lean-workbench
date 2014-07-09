from database import db
import datetime
import time

class Ghosting_model(db.Model):
    """
    Store users that click on features that aren't done yet.
    """
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    feature = db.Column(db.String)
    username = db.Column(db.String)

    def __init__(self, feature, username):
        self.created = datetime.datetime.now()
        self.feature = feature
        self.username = username
