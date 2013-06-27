from flask import Flask
from flask.ext import restful
from app import app
from apps.googleanalytics import Google_analytics_API

class Google_analytics_resource(restful.Resource):
	def get(self, **kwargs):
		args = kwargs.keys()
		if 'start_date' not in args:
			Exception("Must specify start date.")
		if 'end_date' not in args:
			Exception("Must specify end date.")
		if 'metric' in args:
			self.metric = kwargs['metric']
		if self.metric == "percentNewVisits":
			pass

	



