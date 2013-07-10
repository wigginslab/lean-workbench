import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
from flask.ext import restful
from apps.googleanalytics.resources.google_analytics_resource import Google_Analytics_Resource
#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')
app.debug = True
mail = Mail(app)

#APIs
api = restful.Api(app)
api.add_resource(Google_Analytics_Resource, '/api/v1/google-analytics/<string:username>')

