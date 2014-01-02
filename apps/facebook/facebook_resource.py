from flask.ext.restful import fields, marshal_with, abort
import sys
import os
from twiter_model import Twitter_Model, db
from flask.ext.restful import Resource, reqparse
from flask import session, escape

class Facebook_resource(Resource):
	pass