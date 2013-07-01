from flask import Flask
from flask.ext import restful
from app import app
from apps.googleanalytics import Google_analytics_API

class Google_analytics_resource(restful.Resource):
	def get(self, **kwargs):
		
	



