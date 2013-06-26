from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys
from app import app, db

class Google_Analytics_Model(db.Model):
	__tablename__ = "google_analytics"
	uid = db.Column(db.Integer, primary_key=True)
	user = 
	token_expiry = db.Column(db.String)
	access_token = db.Column(db.String)
	client_secret = db.Column(db.String)

