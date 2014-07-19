from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db
import datetime
import time


class Startup_data_model(db.Model):
    __tablename__ = "startup_data"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    angellist_url = db.Column(db.String)
    crunchbase_url = db.Column(db.String)
    # their web presence
    startup_url = db.Column(db.String)
    # leanworkbench username
    username = db.Column(db.String)
    vc_matcher_page = db.Column(db.Integer, default=0)
    vc_matcher_done = db.Column(db.Boolean, default= False)
    description = db.Column(db.Text, default=None)
    vcs = db.relationship('VC_model', backref="startup_data", lazy="dynamic")
    
class VC_model(db.Model):
    __tablename__ = "vc"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    name = db.Column(db.String)
    crunchbase_url = db.Column(db.String)
    angellist_url = db.Column(db.String)
    image_url = db.Column(db.String)
    score = db.Column(db.Integer)
    startup_data_user_id = db.Column(db.Integer, db.ForeignKey('startup_data.id'))


    def as_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'crunchbase_url': self.crunchbase_url,
                'score': self.score
        }
