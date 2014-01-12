import sys
import os
from facebook_model import Facebook_model
from lean_workbench.core import db
from flask.ext.restful import Resource, reqparse, fields, marshal_with, abort
class Facebook_resource(Resource):
	pass