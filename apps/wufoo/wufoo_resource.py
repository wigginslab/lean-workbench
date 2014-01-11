import sys
import os
from wufoo_models import Wufoo_Survey_Model
from flask.ext.restful import Resource, reqparse
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)


db = SQLAlchemy(app)

class Wufoo_resource(Resource):
	pass
