from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from apps.googleanalytics.models.google_analytics_models import *
from apps.googleanalytics.google_analytics_client import Google_Analytics_API
from flask.ext.restful import Resource, reqparse
from flask import session, escape

path = os.getenv("path")
sys.path.append(path)

def check_authentication(username):
	logged_in_user = escape(session.get('username'))
	if username == logged_in_user:
		return True
	else:
		return False


