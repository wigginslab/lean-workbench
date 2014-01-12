import sys
import os
from twitter_model import Twitter_model
from flask.ext.restful import Resource, reqparse
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from database import db


class Twitter_resource(Resource):
	pass
